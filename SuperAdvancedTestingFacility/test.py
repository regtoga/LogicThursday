def get_maxterms(self) -> list:
        maxterms = []
        for col, outputs in enumerate(self.output_values):
            maxterms_for_output = []
            for row, output in enumerate(outputs):
                if int(output.cget("text")) == 0:
                    maxterms_for_output.append(row)
            maxterms.append(maxterms_for_output)

        self.maxterms = maxterms
        #print(self.maxterms)
        return maxterms