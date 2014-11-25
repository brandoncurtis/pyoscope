from numpy import convolve, ones
import matplotlib.pyplot as plot
import sys

def moving_average(interval, window_size):
    """Finds the moving average of a dataset over a window size."""
    # algorithm via http://stackoverflow.com/questions/11352047/finding-moving-average-from-data-points-in-python
    window = ones(int(window_size))/float(window_size)
    return convolve(interval, window, 'same')

def data_import(fileName,fileSeparator,firstRow=1,xCol=1,yCol=2):
    """Imports data from .csv and puts it into an array."""
    dataFile = open(fileName, 'r')
    for i in range(0,firstRow):
        line = dataFile.readline()
    line = dataFile.readline()
    dataReturn = []
    while(line != ''): 
	lineSplit = line.split(fileSeparator)
        dataLine = tuple(float(item.strip()) for item in [lineSplit[int(xCol)-1],lineSplit[int(yCol)-1]])
        dataReturn.append(dataLine)
        line = dataFile.readline()
    return dataReturn
    
def data_pasted(dataString,fileSeparator,firstRow=1,xCol=1,yCol=2):
    """Prepares data that has been copied and pasted into the worksheet from a CSV file."""
    dataList = dataString.splitlines()
    dataReturn = []
    for line in dataList:
	lineSplit = line.split(fileSeparator)
        dataLine = tuple(float(item.strip()) for item in [lineSplit[int(xCol)-1],lineSplit[int(yCol)-1]])
        if len(dataLine)!=0: dataReturn.append(dataLine)
    return dataReturn

def find_area(array):
    """Find the array of a polygon defined as a set of Cartesian points in an array."""
    # algorithm via http://www.arachnoid.com/area_irregular_polygon/index.html
    a = 0
    ox,oy = array[0]
    for x,y in array[1:]:
        a += (x*oy-y*ox)
        ox,oy = x,y
    return abs(a/2)

def create_lissajous(Vapp,Vcap,window=1):
    """Generates a Lissajous figure from the applied and capacitor voltage oscilloscope traces."""
    x=[Vapp[i][1] for i in range(0,len(Vapp))]
    y=[Vcap[i][1] for i in range(0,len(Vcap))]
    if window!= 1:
        x = moving_average(x,window)
        y = moving_average(y,window)
    Liss = []
    for i in range(0,len(Vapp)):
        Liss.append((x[i],y[i]))
    return Liss


if __name__ == '__main__':

    ### for pasted data directly from Tektronix files
    # Vapp = data_pasted(dataString=Vapp,fileSeparator=',',xCol=4,yCol=5) # applied voltage trace
    # Vcap = data_pasted(dataString=Vcap,fileSeparator=',',xCol=4,yCol=5) # series capacitor voltage trace

    ### for the Rigoll PyOscope    
    # Vapp = data_import(fileName=sys.argv[1],fileSeparator='\t',firstRow=6,xCol=1,yCol=2)
    # Vcap = data_import(fileName=sys.argv[2],fileSeparator='\t',firstRow=6,xCol=1,yCol=3)

    ### for imported data from Tektronix files
    Vapp = data_import(fileName=sys.argv[1],fileSeparator=',',firstRow=1,xCol=4,yCol=5)
    Vcap = data_import(fileName=sys.argv[2],fileSeparator=',',firstRow=1,xCol=4,yCol=5)


    windowSize = sys.argv[3]
    Liss = create_lissajous(Vapp=Vapp,Vcap=Vcap,window=windowSize)
    plot.scatter([p[0] for p in Liss], [p[1] for p in Liss])
    plot.show()

    area = find_area(Liss[0:1000])
    print('The area of the Lissajous figure is: ' + str(area))
