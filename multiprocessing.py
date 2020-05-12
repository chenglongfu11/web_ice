

class MultiProcessing:
    def seqprocessing(self):
        # base_building = connectIDA()
        for i in range(6):
            self.testWWR3(i)
            time.sleep(2)

        stat = ida_checkstatus()
        print(stat)