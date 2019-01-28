import sqlalchemy as sa
import sqlahelper
from sqlalchemy import orm
from sqlalchemy.dialects.postgresql import ARRAY, REAL
from sqlalchemy.ext.declarative import declarative_base
import geoalchemy2


SCHEMA = 'coastdat'

Base = declarative_base()
Base.metadata.bind = sqlahelper.get_engine('DB_INTERNAL')


class Timeseries(Base):
    __tablename__ = 'timeseries'
    __table_args__ = {'schema': SCHEMA}

    id = sa.Column(sa.BIGINT, primary_key=True)
    tsarray = sa.Column(ARRAY(REAL))


class Year(Base):
    __tablename__ = 'year'
    __table_args__ = {'schema': SCHEMA}

    year = sa.Column(sa.SMALLINT, primary_key=True)
    leap = sa.Column(sa.BOOLEAN)

    timeseries = orm.relationship(
        'Timeseries', secondary=f'{SCHEMA}.scheduled', backref='year')


class Datatype(Base):
    __tablename__ = 'datatype'
    __table_args__ = {'schema': SCHEMA}

    id = sa.Column(sa.BIGINT, primary_key=True)
    name = sa.Column(sa.VARCHAR)
    description = sa.Column(sa.TEXT)
    height = sa.Column(sa.INTEGER)
    unit = sa.Column(sa.VARCHAR)

    timeseries = orm.relationship(
        'Timeseries', secondary=f'{SCHEMA}.typified', backref='type')


class Spatial(Base):
    __tablename__ = 'spatial'
    __table_args__ = {'schema': SCHEMA}

    gid = sa.Column(sa.BIGINT, primary_key=True)
    geom = sa.Column(geoalchemy2.Geometry('Point', 4326))

    timeseries = orm.relationship(
        'Timeseries', secondary=f'{SCHEMA}.located', backref='spatial')


class Scheduled(Base):
    __tablename__ = 'scheduled'
    __table_args__ = {'schema': SCHEMA}

    data_id = sa.Column(sa.INTEGER, sa.ForeignKey(Timeseries.id))
    time_id = sa.Column(sa.INTEGER, sa.ForeignKey(Year.year))

    sa.PrimaryKeyConstraint(data_id, time_id)


class Typified(Base):
    __tablename__ = 'typified'
    __table_args__ = {'schema': SCHEMA}

    data_id = sa.Column(sa.INTEGER, sa.ForeignKey(Timeseries.id))
    type_id = sa.Column(sa.INTEGER, sa.ForeignKey(Datatype.id))

    sa.PrimaryKeyConstraint(data_id, type_id)


class Located(Base):
    __tablename__ = 'located'
    __table_args__ = {'schema': SCHEMA}

    data_id = sa.Column(sa.INTEGER, sa.ForeignKey(Timeseries.id))
    spatial_id = sa.Column(sa.INTEGER, sa.ForeignKey(Spatial.gid))

    sa.PrimaryKeyConstraint(data_id, spatial_id)


def get_timeseries_join(session):
    ts = session.query(Timeseries)
    ts = ts.join(Scheduled).join(Year)
    ts = ts.join(Located).join(Spatial)
    return ts.join(Typified).join(Datatype)
