import csv

def write_results(file_name, results, labels):
  """
  Writes the results to a csv file descrbed by the file name
  """
  with open(file_name, "w") as output_file:
    writer=csv.writer(output_file)
    for i in range(len(results)):
      writer.writerow([labels[i]]+results[i])