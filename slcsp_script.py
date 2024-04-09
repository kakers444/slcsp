#This program finds the second lowest cost silver plan for a given set of zip codes.
#It only accepts a csv file as the first argument in the command line, and the csv file headers must be zipcode,rate
#If there is ambiguity in the answer based on a zipcode spanning multiple counties with different rates, a blank is returned.
#If there is ambiguity in the answer based on a zipcode spanning multiple states, a blank is also returned.
#Finally, if there are less than 2 different rates found, a blank will be returned.

#The program consists of 2 functions, test_output and find_rate. find_rate is the main function that performs all actions to
#determine the correct csv output in |zipcode, lowest rate| format. test_output is only used to run tests and should be
#expanded in the future to accomodate more tests.

import sys
import csv

def test_output(test, output_data):
    #These tests only access the rate of the first item in the list, always at position 1,1
    #test1 is for a zip code that has no plan rates
    if (test == 'test1'):
        try:
            if (output_data[1][1] == ''):
                sys.stdout.write(f'Test successful, rate was: {output_data[1][1]}')
            else:
                sys.stdout.write(f'Test failed, result was: {output_data[1][1]}')
        except:
            sys.stdout.write('Unknown error in test script.')
            return
        return
    #test2 has multiple plan rates of 6, and should return 212.35
    if (test == 'test2'):
        try:
            if (output_data[1][1] == '212.35'):
                sys.stdout.write(f'Test successful, rate was: {output_data[1][1]}')
            else:
                sys.stdout.write(f'Test failed, result was: {output_data[1][1]}')
        except:
            sys.stdout.write('Unknown error in test script.')
            return
        return
    
    sys.stdout.write('No test data found for this file.')
 
def find_rate(slcsp_input):
    with open('plans.csv') as plans_file, open(slcsp_input) as slcsp_file, open('zips.csv') as zips_file:
        plans_reader = csv.DictReader(plans_file)
        silver_plans = [row for row in plans_reader if row['metal_level'] == 'Silver']
        zips_reader = list(csv.DictReader(zips_file))
    
        slcsp = csv.DictReader(slcsp_file)
        #Ensure that the input file is in the correct format, and then store the header for later output
        if (slcsp.fieldnames != ["zipcode", "rate"]):
            sys.stdout.write('Error - this file does not have the headers zipcode,rate\nOr this file is not a csv file.')
            return
        output_data = [slcsp.fieldnames] 
        
        slcsp_reader = list(slcsp)

        #Perform the rate lookup for each zipcode row in the input file
        for slcsp_row in slcsp_reader:
            #Each zip code may span across multiple counties and rarely states so we filter to get all matches
            filtered_zips = [zip for zip in zips_reader if zip['zipcode'] == slcsp_row['zipcode']]
        
            #Collect all areas and states
            areas = []
            states = []
            for zip_row in filtered_zips:
                areas.append(zip_row['rate_area'])
                states.append(zip_row['state'])

            different_rates = False
            different_states = False

            #Zip codes with more than 1 rate area are considered ambiguous for this program
            if (len(areas) > 1):
                for area in areas:
                    if (areas.count(area) != len(areas)):
                        different_rates = True
                        break

                #make sure to handle the rare case of zipcodes across state lines
                for state in states:
                    if(states.count(state) != len(states)):
                        different_states = True
                        break
        
            if (different_rates or different_states):
                #The rate area cannot be determined for this zip code
                output_data.append([slcsp_row['zipcode'], ''])
            else:
                if (len(filtered_zips) > 0):
                    filtered_plans = [plan for plan in silver_plans if plan['state'] == filtered_zips[0]['state'] and plan['rate_area'] == filtered_zips[0]['rate_area']]
                
                    silver_rates = [float(plan['rate']) for plan in filtered_plans]
                    silver_rates = sorted(silver_rates)

                    #Grab the two lowest rates and handle have multiple of the same rate by not including them in the list
                    two_lowest_rates = []
                    for rate in silver_rates:
                        if (rate not in two_lowest_rates):
                            two_lowest_rates.append(rate)
                            if (len(two_lowest_rates) == 2):
                                break

                    #If there are not at least two unique rates, there cannot be a second lowest and the answer is blank
                    if (len(two_lowest_rates) < 2):
                        output_data.append([slcsp_row['zipcode'], ''])
                    else:
                        #Output the second, highest value to two decimal places
                        output_data.append([slcsp_row['zipcode'], f"{two_lowest_rates[1]:.2f}"])
                else:
                    #If the zip code is not found at all, default to blank
                    output_data.append([slcsp_row, ''])
                
        writer =  csv.writer(sys.stdout)
        
        #Before printing final output, determine if this is a test run. If the user entered a third argument it should be in format testX
        #If the third argument is not a test, default to normal output
        if (len(sys.argv) == 3):
            test = sys.argv[2]
            if ('test' in test):
                test_output(test, output_data)
            else:
                writer.writerows(output_data)
        else:
            writer.writerows(output_data)

if __name__ == '__main__':
    if (len(sys.argv) < 2):
        sys.stdout.write('Please provide an input file in csv format as the first argument.')
    else:
        slcsp_input = sys.argv[1]
        find_rate(slcsp_input)

