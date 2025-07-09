from typing import List
from dagster import (
    asset,
    AssetExecutionContext,
    AssetIn,
    Definitions,
    define_asset_job,
    AssetSelection,
    ScheduleDefinition,
)


@asset(group_name="my_first_group")
def my_first_asset(context: AssetExecutionContext):
    """
    test description
    """
    print("test print message")
    context.log.info("this is a log message")
    return [1, 2, 3]


@asset(group_name="my_second_group")
def my_second_asset(
    context: AssetExecutionContext, my_first_asset: List
):  # Method 1 of using return from another asset
    """
    test description
    """
    data = my_first_asset + [4, 5, 6]
    print("second test message")
    context.log.info(f"output data is: {data}")
    return data


@asset(ins={"upstream": AssetIn(key="my_first_asset")}, group_name="my_second_group")
def my_third_asset(
    context: AssetExecutionContext, upstream: List
):  # Method 2 of using return from another asset
    """
    test description
    """
    data = [7, 8, 9]
    print("third test message")
    context.log.info(f"output data is: {data}")
    return data


# @asset(deps=[my_second_asset, my_third_asset]) #Multiple asset dependancy
@asset(
    ins={
        "first_upstream": AssetIn(key="my_second_asset"),
        "second_upstream": AssetIn(key="my_third_asset"),
    },
    group_name="my_second_group",
)  # Using return from multiple assets
def my_forth_asset(
    context: AssetExecutionContext, first_upstream: List, second_upstream: List
):
    """
    test description
    """
    data = first_upstream + second_upstream
    print("forth test message")
    context.log.info(f"output data is: {data}")


defs = Definitions(
    assets=[my_first_asset, my_second_asset, my_third_asset, my_forth_asset],
    jobs=[
        define_asset_job(
            name="hello_dagster_job",
            # selection=[my_first_asset,my_second_asset,my_third_asset,my_forth_asset]
            # selection=AssetSelection.groups(my_first_group, my_second_group)
            selection=AssetSelection.all(),
        )
    ],
    schedules=[
        ScheduleDefinition(
            name="hello_dagster_schedule",
            job_name="hello_dagster_job",
            cron_schedule="0 10 * * *",
        )
    ],
)
