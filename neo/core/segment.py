from neo.core.baseneo import BaseNeo

import numpy as np

class Segment(BaseNeo):
    """
    A Segment is a heterogeneous container for discrete or continous data
    sharing a common clock (time basis) but not necessary the same sampling rate,
    start or end time.

    *Usage*:
    
    TODO
    
    *Required attributes/properties*:
        None
    
    *Recommended attributes/properties*:
        :name: A label for the dataset 
        :description: text description
        :file_origin: filesystem path or URL of the original data file.
        :file_datetime: the creation date and time of the original data file.
        :rec_datetime: the date and time of the original recording
        :index: integer. You can use this to define a temporal ordering of
            your Segment. For instance you could use this for trial numbers.
    
    *Container of*:
        :py:class:`Epoch`
        :py:class:`EpochArray`
        :py:class:`Event`
        :py:class:`EventArray`
        :py:class:`AnalogSignal`
        :py:class:`AnalogSignalArray`
        :py:class:`IrregularlySampledSignal`
        :py:class:`Spike`
        :py:class:`SpikeTrain`

    """
    def __init__(self, name=None, description=None, file_origin=None,
                 file_datetime=None, rec_datetime=None, index=None, **annotations):
        BaseNeo.__init__(self, name=name, file_origin=file_origin,
                         description=description, **annotations)
        self.file_datetime = file_datetime
        self.rec_datetime = rec_datetime
        self.index = index        
        
        self.epochs = [ ]
        self.epocharrays = [ ]
        self.events = [ ]
        self.eventarrays = [ ]
        self.analogsignals = [ ]
        self.analogsignalarrays = [ ]
        self.irregularlysampledsignals = [ ]
        self.spikes = [ ]
        self.spiketrains = [ ]
        
        self.block = None
    
    def take_spiketrains_by_unit(self, unit_list = [ ]):
        st_list = [ ]
        for st in self.spiketrains:
            if st.unit in unit_list:
                st_list.append(st)
        return st_list
    
    
    def take_analogsignal_by_unit(self, unit_list):
        """
        This assert that Unit.channel_index are the same than AnalogSIgnal.channel_index
        """
        channel_indexes = [ ]
        for unit in unit_list:
            channel_indexes.extend(unit.channel_indexes)
        return self.take_analogsignal_by_channelindex(channel_indexes)
    
    
    def take_analogsignal_by_channelindex(self, channel_indexes):
        anasig_list = [ ]
        for anasig in self.analogsignals:
            if anasig.channel_index in channel_indexes:
                anasig_list.append(anasig)
        return anasig_list
    
    
    def take_slice_of_analogsignalarray_by_unit(self, unit_list):
        sub_indexes = [ ]
        for unit in unit_list:
            sub_indexes.extend(unit.channel_indexes)
        
        sliced_sigarrays = [ ]
        for sigarr in self.analogsignalarrays:
            ind = np.in1d(sigarr.channel_indexes, sub_indexes)
            sliced_sigarrays.append(sigarr[:, ind])
        
        return sliced_sigarrays
    
    
    def construct_subsegment_by_unit(self, unit_list):
        """
        Return AnalogSignal list in a given segment given there Unit parents.
        
        *Example*::
            
            # construction
            nb_seg = 3
            nb_unit = 5
            unit_with_sig = [0, 2, 3]
            signal_types = ['Vm', 'Conductances']
            
            #recordingchannelgroups
            rcgs = [ RecordingChannelGroup(name = 'Vm', channel_indexes = unit_with_sig), 
                            RecordingChannelGroup(name = 'Conductance', channel_indexes = unit_with_sig), ]
            
            # Unit
            all_unit = [ ]
            for u in range(nb_unit):
                un = Unit(name = 'Unit #{}'.format(j), channel_index = u)
                all_unit.append(un)
            
            bl = block()
            for s in range(nb_seg):
                seg = Segment(name = 'Simulation {}'.format(s))
                for j in range(nb_unit):
                    st = SpikeTrain([1, 2, 3], units = 'ms', t_start = 0., t_stop = 10)
                    st.unit = all_unit[j]
                
                for t in signal_types:
                    anasigarr = AnalogSignalArray( zeros(10000, len(unit_with_sig) ))
            
        """
        seg = Segment()
        seg.analogsignals = self.take_analogsignal_by_unit(unit_list)
        seg.spiketrains = self.take_spiketrains_by_unit(unit_list)
        seg.analogsignalarrays = self.take_slice_of_analogsignalarray_by_unit(unit_list)
        #TODO copy others attributes
        return seg


