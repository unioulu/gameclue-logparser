import csv
import counter


# Write a .csv file to args.o output folder
def generate(logfile):
    outputfilepath = f'{logfile}-report.csv'
    print(outputfilepath)

    with open(outputfilepath, 'w+', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='"',
                            quoting=csv.QUOTE_ALL)

        # TODO: write header line to csv

        # Parse some values, such as total shots fired
        normalshots = counter.countKeys(logfile, "PlayerFiredNormalShot")

        # Write report lines
        writer.writerow([normalshots])
