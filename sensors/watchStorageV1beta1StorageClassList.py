from os import sys, path
if __name__ == '__main__' and __package__ is None:
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from sensor_base import SensorBase


class watchStorageV1beta1StorageClassList(SensorBase):

    def __init__(
            self,
            sensor_service,
            config=None,
            extension="/apis/storage.k8s.io/v1beta1/watch/storageclasses",
            trigger_ref="kubernetes.storageclasses"):
        super(
            self.__class__,  # pylint: disable=bad-super-call
            self).__init__(
            sensor_service=sensor_service,
            config=config,
            extension=extension,
            trigger_ref=trigger_ref)
