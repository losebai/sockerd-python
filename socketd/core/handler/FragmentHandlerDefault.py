from ..config.Config import Config
from FragmentHandler import FragmentHandler
from ..module.Entity import Entity
from io import BytesIO


class FragmentHandlerDefault(FragmentHandler):
    def __init__(self):
        pass

    def nextFragment(self, config: Config, fragmentIndex: int, entity: Entity) -> Entity:
        # fragmentIndex.set(fragmentIndex.get() + 1)

        fragmentBuf = BytesIO()
        # IoUtils.transferTo(entity.getData(), fragmentBuf, 0, Config.MAX_SIZE_FRAGMENT)
        fragmentBytes = fragmentBuf.toByteArray()
        if len(fragmentBytes) == 0:
            return None
        fragmentEntity = EntityDefault().data(fragmentBytes)
        if fragmentIndex.get() == 1:
            fragmentEntity.metaMap(entity.getMetaMap())
        fragmentEntity.putMeta(EntityMetas.META_DATA_FRAGMENT_IDX, str(fragmentIndex))
        return fragmentEntity

    def aggrFragment(self, channel, index: int, frame: Frame) -> Frame:
        aggregator = channel.getAttachment(frame.getMessage().getSid())
        if aggregator == None:
            aggregator = FragmentAggregator(frame)
            channel.setAttachment(aggregator.getSid(), aggregator)

        aggregator.add(index, frame)

        if aggregator.getDataLength() > aggregator.getDataStreamSize():
            return None  # Length is not enough, wait for the next fragment package
        else:
            return aggregator.get()  # Reset as a merged frame


class FragmentAggregator():
    def __init__(self, frame: Frame):
        self.fragments = []
        self.sid = frame.getMessage().getSid()
        self.message = frame.getMessage()

    def add(self, index: int, frame: Frame):
        self.fragments.append((index, frame))

    def getDataLength(self) -> int:
        length = 0
        for fragment in self.fragments:
            length += len(fragment[1].getEntity().getData())
        return length

    def getDataStreamSize(self) -> int:
        if len(self.fragments) == 0:
            return 0
        else:
            return len(self.fragments[0][1].getEntity().getData())

    def get(self) -> Frame:
        length = self.getDataLength()
        entityBytes = bytearray(length)

        for fragment in self.fragments:
            entity = fragment[1].getEntity()
            data = entity.getData()
            index = fragment[0]
            size = len(data)
            start = index * size
            end = start + size
            entityBytes[start:end] = data

        return Frame(Frame.Flag.Message, self.message.clone().entity(EntityDefault().data(entityBytes)))
