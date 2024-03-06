from csv import reader
from datetime import datetime
from domain.accelerometer import Accelerometer
from domain.gps import Gps
from domain.aggregated_data import AggregatedData
from domain.parking import Parking
import config


class FileDatasource:
    def __init__(
        self,
        accelerometer_filename: str,
        gps_filename: str,
        parking_filename: str
    ) -> None:
        self.accelerometer_filename = accelerometer_filename
        self.gps_filename = gps_filename
        self.parking_filename = parking_filename

        self.accelerometer_data = None
        self.gps_data = None
        self.parking_data = None

        self.accelerometer_datalist = []
        self.gps_datalist = []
        self.parking_datalist = []

        self.accelerometer_datalist_index = 0
        self.gps_datalist_index = 0
        self.parking_datalist_index = 0

    def read(self) -> AggregatedData:
        try:
            accelerometer_data = self.accelerometer_datalist[self.accelerometer_datalist_index]
            self.accelerometer_datalist_index += 1
        except IndexError:
            self.accelerometer_datalist_index = 0
            accelerometer_data = self.accelerometer_datalist[self.accelerometer_datalist_index]
        try:
            gps_data = self.gps_datalist[self.gps_datalist_index]
            self.gps_datalist_index += 1
        except IndexError:
            self.gps_datalist_index = 0
            gps_data = self.gps_datalist[self.gps_datalist_index]
        try:
            parking_data = self.parking_datalist[self.parking_datalist_index]
            self.parking_datalist_index += 1
        except IndexError:
            self.parking_datalist_index = 0
            parking_data = self.parking_datalist[self.parking_datalist_index]

        return AggregatedData(
            Accelerometer(*accelerometer_data),
            Gps(*gps_data),
            Parking(parking_data[0],Gps(parking_data[1],parking_data[2])),
            datetime.now(),
            config.USER_ID,
        )


    def startReading(self, *args, **kwargs):
        # Accelerometer
        with open(self.accelerometer_filename) as file:
            accelerometer_reader = reader(file)
            next(accelerometer_reader) # Skip header
            for row in accelerometer_reader:
                self.accelerometer_datalist.append(row)
        # GPS
        with open(self.gps_filename) as file:
            gps_reader = reader(file)
            next(gps_reader) # Skip header
            for row in gps_reader:
                self.gps_datalist.append(row)
        # Parking
        with open(self.parking_filename) as file:
            parking_reader = reader(file)
            next(parking_reader) # Skip header
            for row in parking_reader:
                self.parking_datalist.append(row)


    def stopReading(self, *args, **kwargs):
        """Метод повинен викликатись для закінчення читання даних"""
