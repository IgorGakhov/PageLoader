from progress.bar import IncrementalBar


class Progress:
    '''Displays the progress of downloading resources to the terminal.'''
    def __init__(self, count: int) -> None:
        self.bar = IncrementalBar(
            'Resources Loading',
            max=count,
            suffix=f'%(percent)d%%   [{IncrementalBar.suffix}]\n'
        )

    def downloading_resources_next(self) -> None:
        self.bar.next()

    def downloading_resources_finish(self) -> None:
        self.bar.finish()
