class Stream:
    def __init__(self, quiet):
        """
        Set up quiet mode
        """
        self.quiet = quiet

    def display(self, logs):
        '''
        Display in stdout depending on the Stream Generator
        It also considers when the stream is targeting a line, to reproduce
        what there are in the original docker binary.
        '''
        lines = {}
        previous_len = 0
        for log in logs:
            if self.quiet:
                continue

            if 'stream' in log:
                print(log['stream'])
                # reset lines
                lines = {}
            if 'status' in log:
                if 'id' not in log:
                    log['id'] = '0'

                if 'progress' in log:
                    lines[log['id']] = log['status'] + ' ' + log['progress']
                else:
                    lines[log['id']] = log['status']

                if previous_len > 0:
                    print('\033[F' * previous_len, end='')
                previous_len = len(lines)
                for line in lines.values():
                    print('\033[K', end='')
                    print(line, end='\n')
                print(end='\r')

        print('')
