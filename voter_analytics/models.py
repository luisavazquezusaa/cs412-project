from django.db import models

# Create your models here.

class Voter (models.Model):
    first_name = models.TextField(blank = True)
    last_name = models.TextField(blank = True)
    address_street_number = models.IntegerField(blank= True)
    address_street_name = models.TextField(blank = True)
    address_apartment_number = models.IntegerField(blank= True, null=True)
    address_zip_code = models.IntegerField(blank= True)
    date_birth = models.DateField(blank= True)
    date_registration = models.DateField(blank= True, null=True) 
    party = models.CharField(max_length=2, blank=True, null=True) 
    precinct_number = models.CharField(max_length=10, blank=True, null=True)
    v20state = models.IntegerField(blank=True, null=True)
    v21town = models.IntegerField(blank=True, null=True)
    v21primary = models.IntegerField(blank=True, null=True)
    v22general = models.IntegerField(blank=True, null=True)
    v23town = models.IntegerField(blank=True, null=True)
    voter_score = models.IntegerField(default=0)

    def __str__(self):
        return (
            f"Full name: {self.first_name} {self.last_name}, "
            f"Date of Birth: {self.date_birth}, "
            f"Address: {self.address_street_number} {self.address_street_name} Apt {self.address_apartment_number}, "
            f"Zip: {self.address_zip_code}, Party: {self.party}"
        )



def load_data():
    '''Function to load data records from CSV file into Django model instances.'''

    ## very dangerous!
    #Voter.objects.all().delete()

    filename = '/Users/luisavazquezusabiaga/django/newton_voters.csv'
    f = open(filename, 'r') # open the file for reading

    # discard headers:
    f.readline() # do nothing with it

    # read several rows
    # for i in range(5):
        # line = f.readline()

    # read entire file, one line at the time
    for line in f:

        try: 

            fields = line.strip().split(',')
            # print(fields)
            # for j in range(len(fields)):
            #     print(f'fields[{j}] = {fields[j]}') 

            # create a new instance of Result object with this record from CSV
            voter = Voter(
                last_name = fields[1],
                first_name = fields[2],
                address_street_number = fields[3],
                address_street_name = fields[4],
                address_apartment_number = fields[5] or None,
                address_zip_code = fields[6],
                date_birth = fields[7],
                date_registration = fields[8],
                party = fields[9],
                precinct_number = fields[10],
                v20state = 1 if fields[11].upper() == 'TRUE' else 0,
                v21town = 1 if fields[12].upper() == 'TRUE' else 0,
                v21primary = 1 if fields[13].upper() == 'TRUE' else 0,
                v22general = 1 if fields[14].upper() == 'TRUE' else 0,
                v23town = 1 if fields[15].upper() == 'TRUE' else 0,
                voter_score = fields[16],
            )
            
            voter.save() # commit to database
            #print(f'Created result: {result}.')
        
        except Exception as e: 
            print("Something went wrong!", e)
            print(f"line={line}")
        
    print(f"Created {len(Voter.objects.all())} Voters")

