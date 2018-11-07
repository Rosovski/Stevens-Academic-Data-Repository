import datetime,unittest

def date_arithmetic():
    """give back the result of three days after Feb 27, 2000, three days after Feb 27, 2017,
       How many days passed between Jan 1, 2017 and Oct 31, 2017
    """
    date1,date2,date3,date4 = "Feb 27, 2000","Feb 27, 2017","Jan 1, 2017","Oct 31, 2017"
    #get the string of date and convert into a format of date object
    dt1 = datetime.datetime.strptime(date1, '%b %d, %Y')
    dt2 = datetime.datetime.strptime(date2, '%b %d, %Y')
    dt3 = datetime.datetime.strptime(date3, '%b %d, %Y')
    dt4 = datetime.datetime.strptime(date4, '%b %d, %Y')
    
    dt1_str = dt1.strftime('%b %d, %Y')
    dt2_str = dt2.strftime('%b %d, %Y')
    dt3_str = dt3.strftime('%b %d, %Y')
    dt4_str = dt4.strftime('%b %d, %Y')
    
    num_days = 3 # three days after two given dates
    dt1_new = dt1 + datetime.timedelta(days = num_days)
    dt2_new = dt2 + datetime.timedelta(days = num_days)
    
    print('{} days after {} is {}'.format(num_days,dt1_str,dt1_new.strftime('%b %d, %Y')))
    print('{} days after {} is {}'.format(num_days,dt2_str,dt2_new.strftime('%b %d, %Y')))
    
    delta = dt4 - dt3 # the interval bewteen two dates
    print('{} days passed bewteen {} and {}'.format(delta.days,dt3_str,dt4_str))

def file_reader(path,number,sep = ',',header = 'False'):
    """get each line in the file, seperated by a given seperation, 
       skip the first line if the header is true,
       yield every line when the function is called
    """
    try:
        fp = open(path,'r')
    except FileNotFoundError:
        print("Cannot open ",path)
    else:
        with fp:
            line_num = 1 # start from the first line of the file
            
            if header == True: # if header exists, skip the first line and start from the second
                next(fp) 
                line_num += 1          
            
            for line in fp:
                content = line.rstrip('\r\n').split(sep)
                if len(content) != number:
                    raise ValueError("'{}' has {} fields on line {} but expected {}".format(path,len(content),line_num,number))
                
                yield content
                line_num += 1

class FileReaderTest(unittest.TestCase):
    def test_generator(self):
        gen = file_reader("123.txt", 3, ";", True)
        self.assertEqual(next(gen), ["donuts", "sandwich", "omelette"])
        self.assertEqual(next(gen), ["jpmorgan", "merrilllynch", "morganstanley"])
        with self.assertRaises(StopIteration):
            next(gen)

    def test_generator_noexist(self):
        gen = file_reader("jr.txt", 3, ";", True)
        with self.assertRaises(StopIteration):
            next(gen)                                                                                    
                                                                                                                                                                           
if __name__ == '__main__':
    unittest.main(verbosity=2)               