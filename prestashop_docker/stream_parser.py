class StreamParser:
    def __init__(self):
        pass

    def display(self, logs):
        lines = {}
        previous_len = 0
        for log in logs:
            if 'stream' in log:
                print(log['stream'])
            if 'status' in log:
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
