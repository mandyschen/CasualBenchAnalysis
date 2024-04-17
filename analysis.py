import json
import os
import math
import xlsxwriter
 
def iterate():
    data_directory = "./k562_Metrics"
    workbook = xlsxwriter.Workbook('k562.xlsx')
    worksheet_25 = workbook.add_worksheet("0.25")
    worksheet_50 = workbook.add_worksheet("0.50")
    worksheet_75 = workbook.add_worksheet("0.75")
    worksheet_100 = workbook.add_worksheet("1.00")
    row25 = 1
    row50 = 1
    row75 = 1
    row100 = 1
    for models in os.listdir(data_directory):
        if models == ".DS_Store":
            continue
        test_directory = data_directory + "/" + models
        for tests in os.listdir(test_directory):
            json_files_directory = data_directory + "/" + models + "/" + tests

            # different sheets
            fraction_partial_intervention = ""
            # parameters that will be recorded
            model_name = ""
            true_positives = ""
            false_positives = ""
            wasserstein_distance = ""
            run_time = ""

            for json_files in os.listdir(json_files_directory):
                if json_files == "arguments.json":
                    f = open(data_directory + "/" + models + "/" + tests + "/" + json_files)
                    data = json.load(f)
                    model_name = data["model_name"]
                    fraction_partial_intervention = data["fraction_partial_intervention"]
                    f.close()
                elif json_files == "metrics.json":
                    f = open(data_directory + "/" + models + "/" + tests + "/" + json_files)
                    data = json.load(f)
                    true_positives = data["quantitative_test_evaluation"]["output_graph"]["true_positives"]
                    false_positives = data["quantitative_test_evaluation"]["output_graph"]["false_positives"]
                    wasserstein_distance = data["quantitative_test_evaluation"]["output_graph"]["wasserstein_distance"]["mean"]
                    if math.isnan(wasserstein_distance):
                        wasserstein_distance = -1
                    run_time = data["run_time"]
                    f.close()
            
            # print in terminal different values
            print(model_name + " " + str(fraction_partial_intervention) + " " + str(true_positives) + " " + str(false_positives) + " " + str(wasserstein_distance) + " " + str(run_time))
            
            worksheet = worksheet_100
            row = row100
            if fraction_partial_intervention == 0.25:
                worksheet = worksheet_25
                row = row25
            elif fraction_partial_intervention == 0.5:
                worksheet = worksheet_50
                row = row50
            elif fraction_partial_intervention == 0.75:
                worksheet = worksheet_75
                row = row75

            worksheet.write(0, 0, "model_name")
            worksheet.write(0, 1, "true_positives")
            worksheet.write(0, 2, "false_positives")
            worksheet.write(0, 3, "wasserstein_distance")
            worksheet.write(0, 4, "run_time")

            worksheet.write(row, 0, model_name)
            worksheet.write(row, 1, true_positives)
            worksheet.write(row, 2, false_positives)
            worksheet.write(row, 3, wasserstein_distance)
            worksheet.write(row, 4, run_time)
            if fraction_partial_intervention == 0.25:
                row25 += 1
            elif fraction_partial_intervention == 0.5:
                row50 += 1
            elif fraction_partial_intervention == 0.75:
                row75 += 1
            elif fraction_partial_intervention == 1.0:
                row100 += 1

    workbook.close()

iterate()