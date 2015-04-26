
class Timeline:
    def __init__(self, timeline):
        self._timeline = timeline

        self.entry_count = len(self._timeline)
        self.position = 0

    def __iter__(self):
        return self

    def next(self):
        try:
            ret = TimelineEntry(self._timeline[self.position]) 
        except IndexError:
            raise StopIteration

        self.position += 1

        return ret


class TimelineEntry:
    def __init__(self, data):
        self._data = data

    def __repr__(self):
        ret = u"\nTimestamp\t%s\n" % self.timestamp

        ret += "Type\t\t"
        if self.is_ioc:
            ret += "IOC "
        ret += "%s" % self.entry_type

        if self.entry_type in ['FileModification',
                               'RegistryModification',
                               'Process']:

            if self.entry_type == 'FileModification':
                ret += " (%s)\n" % self.modification
            else:
                ret += "\n"

            if self.path:
                ret += "Path\t\t%s" % self.path

            if self.md5:
                ret += "\nMD5\t\t%s" % self.md5

        if self.entry_type == 'NetworkConnection':

            ret += " (%s)\n" % self.direction

            if self.domain:
                ret += "Domain\t\t%s\n" % self.domain

            if self.ip:
                ret += "IP\t\t%s\n" % self.ip

            ret += "Port\t\t%s\n" % self.port

            ret += "Protocol\t%s" % self.protocol_name

        return ret.encode('UTF-8')

    @property
    def timestamp(self):
        return self._data['timestamp']

    @property
    def entry_type(self):
        return self._data['type']

    @property
    def ip(self):
        ret = None
        if self._data.has_key('ip'):
            ret = self._data['ip']

        return ret

    @property
    def domain(self):
        ret = None
        if self._data.has_key('domain'):
            ret = self._data['domain']

        return ret

    @property
    def protocol(self):
        ret = None
        if self._data.has_key('protocol'):
            ret = self._data['protocol']

        return ret

    @property
    def protocol_name(self):
        ret = None
        if self._data.has_key('protocol'):
            n = self._data['protocol']

            if n == '6':
                ret = 'TCP'
            elif n == '17':
                ret = 'UDP'

        return ret

    @property
    def direction(self):
        ret = None
        if self._data.has_key('direction'):
            ret = self._data['direction']

        return ret
        
    @property
    def port(self):
        ret = None
        if self._data.has_key('port'):
            ret = self._data['port']

        return ret
        
    @property
    def modification(self):
        ret = None
        if self._data.has_key('modification'):
            ret = self._data['modification']

        return ret

    @property
    def is_ioc(self):
        """None: A metadata element, such as time of occurence or time of
            analyst confirmation.

           True: Entry is an IOC.

           False: Entry is not an IOC.
        """
        ret = None
        if self._data.has_key('is_ioc'):
            ret = self._data['is_ioc']

        return ret

    @property
    def path(self):
        ret = None
        if self.entry_type in ['Process', 
                               'FileModification',
                               'RegistryModification']:
            ret = self._data['path']

        return ret

    @property
    def md5(self):
        ret = None
        if self._data.has_key('md5'):
            ret = self._data['md5']

        return ret
