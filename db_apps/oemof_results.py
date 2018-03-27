
import pandas
from sqlalchemy import (
    Column, Integer, String, ARRAY, ForeignKey)
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION
from sqlalchemy.ext.declarative import declarative_base
from oemof.outputlib.processing import convert_keys_to_strings

"""
Module to store and restore input- and result-data from oemof into database.
Works with oemof version 2.0

Notes
-----
By now, table names are static - if you are not satisfied with resulting 
table names, you have to change code yourself!

Examples
--------
The following code will setup your sqlalchemy session and 
create all needed tables in database:
>>> from sqlalchemy import orm
>>> import sqlahelper

>>> engine = sqlalchemy.create_engine(db_url)
>>> sqlahelper.add_engine(engine)
>>> SqlAlchemySession = orm.sessionmaker(bind=engine)
>>> from db_apps.oemof_results import Base
>>> Base.metadata.bind = engine
>>> Base.metadata.create_all()

The following code stores your data into DB:
>>> sa_session = SqlAlchemySession()
>>> store_results(sa_session, input_dict, result_dict)
>>> sa_session.close()

The following code restores your data from DB:
>>> sa_session = SqlAlchemySession()
>>> input_dict, result_dict = restore_results(sa_session, result_id)
>>> sa_session.close()
"""

Base = declarative_base()


class OemofInputResult(Base):
    __tablename__ = 'stemp_oemof_input_result'

    input_result_id = Column(
        Integer,
        primary_key=True
    )
    input_id = Column(Integer, ForeignKey('stemp_oemof_data.data_id'))
    result_id = Column(Integer, ForeignKey('stemp_oemof_data.data_id'))
    input = relationship(
        "OemofData",
        backref="input",
        uselist=False,
        foreign_keys=[input_id],
    )
    result = relationship(
        "OemofData",
        backref="result",
        uselist=False,
        foreign_keys=[result_id],
    )


class OemofData(Base):
    __tablename__ = 'stemp_oemof_data'

    data_id = Column(
        Integer,
        primary_key=True
    )
    scalars = relationship("OemofScalar", cascade="delete")
    sequences = relationship("OemofSequence", cascade="delete")


class OemofScalar(Base):
    __tablename__ = 'stemp_oemof_scalar'

    scalar_id = Column(
        Integer,
        primary_key=True
    )
    data_id = Column(
        Integer, ForeignKey('stemp_oemof_data.data_id'))
    from_node = Column(
        String
    )
    to_node = Column(
        String
    )
    attribute = Column(
        String
    )
    value = Column(
        String
    )
    type = Column(
        String
    )


class OemofSequence(Base):
    __tablename__ = 'stemp_oemof_sequence'

    sequence_id = Column(
        Integer,
        primary_key=True
    )
    data_id = Column(
        Integer, ForeignKey('stemp_oemof_data.data_id'))
    from_node = Column(
        String
    )
    to_node = Column(
        String,
        nullable=True
    )
    attribute = Column(
        String
    )
    value = Column(
        ARRAY(DOUBLE_PRECISION)
    )
    type = Column(
        String
    )


def store_results(session, input_data, result_data):
    """
    Stores inputs and results from oemof into DB

    For each in entry in scalars and sequences of both input- and result-data
    an OemofScalar or OemofSequence is build and connected to an OemofData
    object representing either input or result data. At last, both OemofData
    objects are connected to OemofInputResult object and resulting index is
    returned.

    Parameters
    ----------
    session: sqlalchemy.session
        SQLAlchemy session build via sqlalchemy.orm.sessionmaker
    input_data: dict
        Output of oemof.outputlib.processing.param_results with nodes as str
        (use oemof.outputlib.processing.convert_keys_to_str if necessary)
    result_data: dict
        Output of oemof.outputlib.processing.param_results with nodes as str
        (use oemof.outputlib.processing.convert_keys_to_str if necessary)

    Returns
    -------
    int: Index of created OemofInputResult entry
    """
    # Check if nodes are strings:
    if not isinstance(next(iter(input_data)), str):
        input_data = convert_keys_to_strings(input_data)
    if not isinstance(next(iter(result_data)), str):
        result_data = convert_keys_to_strings(result_data)

    input_result = OemofInputResult()
    for input_result_attr, data in (
            ('input', input_data), ('result', result_data)):
        scalars = []
        sequences = []
        for (from_node, to_node), sc_sq_dict in data.items():
            for key, value in sc_sq_dict['scalars'].items():
                scalars.append(
                    OemofScalar(
                        from_node=from_node,
                        to_node=to_node,
                        attribute=key,
                        value=value,
                        type=type(value).__name__
                    )
                )
            session.add_all(scalars)
            for key, series in sc_sq_dict['sequences'].items():
                list_type = 'list'
                if isinstance(series, pandas.Series):
                    series = series.values.tolist()
                    list_type = 'series'
                sequences.append(
                    OemofSequence(
                        from_node=from_node,
                        to_node=to_node,
                        attribute=key,
                        value=series,
                        type=list_type
                    )
                )
            session.add_all(sequences)
        oemof_data = OemofData()
        oemof_data.scalars = scalars
        oemof_data.sequences = sequences
        setattr(input_result, input_result_attr, oemof_data)
    session.add(input_result)
    session.flush()
    result_id = input_result.input_result_id
    session.commit()
    return result_id


def restore_results(session, input_result_id):
    """
    Restores input and result data from OemofInputResult from DB

    Parameters
    ----------
    session: sqlalchemy.session
        SQLAlchemy session build via sqlalchemy.orm.sessionmaker
    input_result_id: int
        Index of OemofInputResult object to restore

    Returns
    -------
    (dict, dict):
        Restored input- and result-data
    """
    def type_conversion(value_str, value_type):
        if value_type == 'str':
            return value_str
        elif value_type == 'float':
            return float(value_str)
        elif value_type == 'int':
            return int(value_str)
        elif value_type == 'bool':
            return bool(value_str)
        else:
            raise TypeError('Unknown conversion type "' + value_type + '"')

    # Find results:
    input_result = session.query(OemofInputResult).filter(
        OemofInputResult.input_result_id == input_result_id).first()
    if input_result is None:
        raise IndexError(
            'Could not find OemofInputResult with ID #' + str(input_result_id))

    input_data = {}
    result_data = {}
    for input_result_attr, data in (
            ('input', input_data), ('result', result_data)):
        ir_attr = getattr(input_result, input_result_attr)
        for scalar in ir_attr.scalars:
            nodes = (scalar.from_node, scalar.to_node)
            if nodes not in data:
                data[nodes] = {'scalars': {}, 'sequences': {}}
            data[nodes]['scalars'][scalar.attribute] = type_conversion(
                scalar.value, scalar.type)
        for sequence in ir_attr.sequences:
            nodes = (sequence.from_node, sequence.to_node)
            if nodes not in data:
                data[nodes] = {'scalars': {}, 'sequences': {}}
            if sequence.type == 'series':
                series = pandas.Series(sequence.value)
            else:
                series = sequence.value
            data[nodes]['sequences'][sequence.attribute] = series
    return input_data, result_data
