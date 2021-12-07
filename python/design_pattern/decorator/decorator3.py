

class Repeat:
    def __init__(self, counts):
        self.repeat_counts = counts  


    def __call__(self, func):

        def wrapper(*arg, **kwargs):
            for _ in range(0, self.repeat_counts):
                func(*arg, **kwargs)

        return wrapper



class Wave:
    def __init__(self):
        pass


    def __call__(self, func):

        def wrapper(*arg, **kwargs):
            print('~~~')
            func(*arg, **kwargs)
            print('+++')

        return wrapper


@Repeat(3)
@Wave()
def main():
    print('hello decorator.')


if __name__ == '__main__':
    main()
