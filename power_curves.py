import preparation

turbine_data = preparation.prepare_turbine_data(data_name="turbine_data")

enercon_data = turbine_data[turbine_data["Turbine"] == "Enercon E-53"]
gamesa_data = turbine_data[turbine_data["Turbine"] == "Gamesa G97 (2000kW)"]
vestas_data = turbine_data[turbine_data["Turbine"] == "Vestas V-117 (4.2MW)"]
