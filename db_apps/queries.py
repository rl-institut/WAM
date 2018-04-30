
import logging
from stemp.oep_models import OEPScenario
from stemp.scenarios import bhkw_scenario, oil_scenario, pv_heatpump_scenario

logging.getLogger().setLevel(logging.INFO)


def delete_oep_scenario(scenario):
    # Does not work!
    OEPScenario.delete({'scenario': scenario})


def insert_scenarios():
    bhkw_scenario.upload_scenario_parameters()
    oil_scenario.upload_scenario_parameters()
    pv_heatpump_scenario.upload_scenario_parameters()


def recreate_scenarios():
    OEPScenario.delete_table()
    OEPScenario.create_table()
    insert_scenarios()


if __name__ == '__main__':
    recreate_scenarios()
