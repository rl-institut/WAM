
import pandas
from oemof.solph import (
    EnergySystem, Bus, Transformer, Flow, Investment, Sink, Model)
from oemof.solph.components import GenericStorage
from oemof.outputlib import processing
from energysystem.results import Results
from energysystem.oemof_results import (
    get_invest_for_node, get_opex_for_node, get_fuel_costs_for_node,
    get_lcoe_for_node, calculate_lcoe, calculate_costs, Costs, AttributeKey
)


def create_energysystem(periods=2):
    # initialize energy system
    es = EnergySystem(
        timeindex=pandas.date_range('2016-01-01', periods=periods,
                                    freq='H')
    )

    # BUSSES
    b_el1 = Bus(label="b_el1")
    b_el2 = Bus(label="b_el2")
    b_diesel = Bus(label='b_diesel', balanced=False)
    es.add(b_el1, b_el2, b_diesel)

    # TEST DIESEL:
    dg_output = Flow(
                variable_costs=1,
                investment=Investment(ep_costs=0.5)
    )
    dg_output.real_invest_costs = 10
    dg = Transformer(
        label='diesel',
        inputs={
            b_diesel: Flow(
                variable_costs=2,
            )
        },
        outputs={
            b_el1: dg_output
        },
        conversion_factors={b_el1: 2},
    )

    batt = GenericStorage(
        label='storage',
        inputs={b_el1: Flow(variable_costs=3)},
        outputs={b_el2: Flow(variable_costs=2.5)},
        capacity_loss=0.00,
        initial_capacity=0,
        nominal_input_capacity_ratio=1 / 6,
        nominal_output_capacity_ratio=1 / 6,
        inflow_conversion_factor=1,
        outflow_conversion_factor=0.8,
        investment=Investment(ep_costs=0.4),
    )
    batt.real_invest_costs = 30

    demand = [100] * 2
    demand[0] = 0.0
    demand = Sink(
        label="demand_el",
        inputs={
            b_el2: Flow(
                nominal_value=1,
                actual_value=demand,
                fixed=True
            )
        }
    )
    es.add(dg, batt, demand)
    return es


def simulate(es):
    om = Model(energysystem=es)
    om.solve(
        solver='cbc',
        solve_kwargs={'tee': True, 'keepfiles': True},
    )
    return (
        processing.results(om),
        processing.param_results(om, exclude_none=True, keys_as_str=True)
    )


energysystem = create_energysystem()
energysystem.flows()
results = Results(*simulate(energysystem))

additional_costs = [
    Costs(
        'real_costs',
        AttributeKey('scalars', 'invest'),
        AttributeKey('scalars', 'real_invest_costs')
    )
]
costs = calculate_costs(
    results.param_results, results.results, additional_costs)

diesel_results = results.get_node_results('diesel')
diesel_flows = results.get_node_flows('diesel')
storage_results = results.get_node_results('storage')
storage_flows = results.get_node_flows('storage')


class TestLcoe(object):
    def test_invest(self):
        assert get_invest_for_node(diesel_results, diesel_flows) == 62.5 * 0.5
        assert get_invest_for_node(storage_results, storage_flows) == 600 * 0.4

    def test_opex(self):
        assert get_opex_for_node(diesel_results, diesel_flows) == 125
        assert get_opex_for_node(storage_results, storage_flows) == 100 * 2.5

    def test_fuel_costs(self):
        assert get_fuel_costs_for_node(diesel_results, diesel_flows) == 62.5 * 2
        assert get_fuel_costs_for_node(storage_results, storage_flows) == 125 * 3

    def test_lcoe_per_node(self):
        diesel_lcoe = calculate_lcoe('diesel', results.results, costs)
        output = 125
        assert diesel_lcoe.invest == 62.5 * 0.5 / output
        assert diesel_lcoe.output_costs == 125 / output
        assert diesel_lcoe.input_costs == 62.5 * 2 / output

        output = 100
        storage_lcoe = calculate_lcoe('storage', results.results, costs)
        assert storage_lcoe.invest == 600 * 0.4 / output
        assert storage_lcoe.output_costs == (100 * 2.5) / output
        assert storage_lcoe.input_costs == 125 * 3 / output

    def test_real_investment(self):
        assert get_invest_for_node(
            diesel_results, diesel_flows, use_real_costs=True) == 62.5 * 10
        assert get_invest_for_node(
            storage_results, storage_flows, use_real_costs=True) == 600 * 30
