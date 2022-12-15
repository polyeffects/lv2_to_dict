from rdfdict import RDFdict
import namespaces as ns
import rdflib
from pprint import pprint
import sys, subprocess

effect_type_map = { #"granular" : "http://polyeffects.com/lv2/polyclouds#granular",
        #"looping_delay" : "http://polyeffects.com/lv2/polyclouds#looping_delay",
        #"algo_reverb" : "http://polyeffects.com/lv2/polyclouds#oliverb",
        #"resonestor" : "http://polyeffects.com/lv2/polyclouds#resonestor",
        #"spectral_twist" : "http://polyeffects.com/lv2/polyclouds#spectral",
        #"time_stretch" : "http://polyeffects.com/lv2/polyclouds#stretch",
        #"bitmangle" : "http://polyeffects.com/lv2/polywarps#bitcrusher",
        #"chebyschev_waveshaper" : "http://polyeffects.com/lv2/polywarps#chebyschev",
        #"comparator" : "http://polyeffects.com/lv2/polywarps#comparator",
        #"twist_delay" : "http://polyeffects.com/lv2/polywarps#delay",
        #"doppler_panner" : "http://polyeffects.com/lv2/polywarps#doppler",
        #"wavefolder" : "http://polyeffects.com/lv2/polywarps#fold",
        #"frequency_shifter" : "http://polyeffects.com/lv2/polywarps#frequency_shifter",
        #"meta_modulation" : "http://polyeffects.com/lv2/polywarps#meta",
        #"vocoder" : "http://polyeffects.com/lv2/polywarps#vocoder",
        #"diode_ladder_lpf": "http://polyeffects.com/lv2/polyfilter#diode_ladder",
        #"k_org_hpf": "http://polyeffects.com/lv2/polyfilter#korg_hpf",
        #"k_org_lfp": "http://polyeffects.com/lv2/polyfilter#korg_lpf",
        #"oog_half_lpf": "http://polyeffects.com/lv2/polyfilter#moog_half_ladder",
        #"oog_ladder_lpf": "http://polyeffects.com/lv2/polyfilter#moog_ladder",
        #"uberheim_filter": "http://polyeffects.com/lv2/polyfilter#oberheim",
        #"extended_rotary": "http://gareus.org/oss/lv2/b_whirl#extended"
        #"extended_rotary": "http://gareus.org/oss/lv2/b_whirl#simple"
        #"cv_to_cc": "http://polyeffects.com/lv2/cv_to_cc"
       # "midi_clock_in": "http://polyeffects.com/lv2/mclk_in",
        #"midi_clock_out": "http://gareus.org/oss/lv2/mclk"
        #"vca": "http://polyeffects.com/lv2/basic_modular#amp",
        #"difference": "http://polyeffects.com/lv2/basic_modular#difference",
        #"macro_osc": "http://polyeffects.com/lv2/polyplaits",
        #"midi_note_to_cv": "http://polyeffects.com/lv2/midi_to_cv_mono"
        #"two_voice": "http://moddevices.com/plugins/mod-devel/2Voices",
        #"capo": "http://moddevices.com/plugins/mod-devel/Capo",
        #"drop": "http://moddevices.com/plugins/mod-devel/Drop",
        #"harmony": "http://moddevices.com/plugins/mod-devel/Harmonizer",
        #"harmony2": "http://moddevices.com/plugins/mod-devel/Harmonizer2",
        #"harmony_custom": "http://moddevices.com/plugins/mod-devel/HarmonizerCS",
        #"extra_capo": "http://moddevices.com/plugins/mod-devel/SuperCapo",
        #"pitch_wam": "http://moddevices.com/plugins/mod-devel/SuperWhammy",
        #"pitch_detect": "http://polyeffects.com/lv2/pitch_detect",
        #"pitch_corrector" : "http://gareus.org/oss/lv2/fat1",
        #"octaver" : "http://guitarix.sourceforge.net/plugins/gx_oc_2_#_oc_2_",
#        "vinyl": "http://calf.sourceforge.net/plugins/Vinyl",
        #"pitch_shift": "http://moddevices.com/plugins/tap/pitch",
        #"adsr": "http://drobilla.net/plugins/blop/adsr",
        #"sample_hold": "http://avwlv2.sourceforge.net/plugins/avw/samplehold",
        #"dahdsr": "http://drobilla.net/plugins/blop/dahdsr",
        #"drum_patterns" : "http://polyeffects.com/lv2/polygrids"
        # "wet_dry": "http://polyeffects.com/lv2/wet_dry",
        # "wet_dry_stereo": "http://polyeffects.com/lv2/wet_dry_stereo",
        # "ad_envelope": "http://drobilla.net/plugins/omins/adenv",
        #"ad_env_level": "http://drobilla.net/plugins/omins/adenv_lvl",
        # "poly_note_to_cv": "http://polyeffects.com/lv2/midi-to-cv-poly",
        #"beat_repeat": "http://polyeffects.com/lv2/polyclouds#beat_repeat",
        # "tempo_ratio": "http://polyeffects.com/lv2/basic_modular#tempo_ratio",
        # "toggle": "http://polyeffects.com/lv2/basic_modular#toggle",
        # "phaser_ext": "http://polyeffects.com/lv2/stone-phaser-ext",
        #"phaser_stereo_ext": "http://polyeffects.com/lv2/stone-phaser-stereo-ext",
        #"harmonic_tremolo": "http://polyeffects.com/lv2/harm_trem",
        #"harmonic_trem_ext": "http://polyeffects.com/lv2/harm_trem_ext",
        # "chorus_d" : "http://polyeffects.com/lv2/chorus",
        # "chorus_d_ext": "http://polyeffects.com/lv2/chorus_ext",
        # "flanger" : "http://polyeffects.com/lv2/flanger",
        # "flanger_ext" : "http://polyeffects.com/lv2/flanger_ext",
        # "vibrato": "http://polyeffects.com/lv2/vibrato",
        # "vibrato_ext": "http://polyeffects.com/lv2/vibrato_ext",
        #"step_sequencer_ext": "http://polyeffects.com/lv2/step_sequencer",
        #"step_sequencer": "http://polyeffects.com/lv2/step_sequencer_bpm",
        # "quantizer": "http://polyeffects.com/lv2/basic_quantizer",
        #"chaos_controller": "http://polyeffects.com/lv2/polymarbles",
        # "multi_resonator" : "http://polyeffects.com/lv2/polyrings",
        # 'beat_repeat': 'http://polyeffects.com/lv2/polyclouds#beat_repeat',
        #'schmitt_trigger': "http://polyeffects.com/lv2/basic_modular#schmitt",
        #'looping_envelope': 'http://polyeffects.com/lv2/polytides',
        # "cv_meter": "http://moddevices.com/plugins/mod-devel/mod-cv-meter",
        # "pitch_cal_in": "http://polyeffects.com/lv2/pitch_cal#in",
        # "pitch_cal_out": "http://polyeffects.com/lv2/pitch_cal#out",
        #"basic_reverb": "http://distrho.sf.net/plugins/MVerb",
        # "cv_to_note": "http://polyeffects.com/lv2/cv_to_note",
        #"bitcrushed_delay": "http://polyeffects.com/lv2/bitcrushed_delay"
#        "bitcrusher": "http://polyeffects.com/lv2/bitcrusher"
# "midi_cc_to_note": "http://gareus.org/oss/lv2/midifilter#cctonote",
# "midi_channel_filter": "http://gareus.org/oss/lv2/midifilter#channelfilter",
# "midi_channel_map": "http://gareus.org/oss/lv2/midifilter#channelmap",
# "midi_choke_filter": "http://gareus.org/oss/lv2/midifilter#chokefilter",
# "midi_enforce_scale": "http://gareus.org/oss/lv2/midifilter#enforcescale",
# "midi_event_blocker": "http://gareus.org/oss/lv2/midifilter#eventblocker",
# "midi_keyrange": "http://gareus.org/oss/lv2/midifilter#keyrange",
# "midi_keysplit": "http://gareus.org/oss/lv2/midifilter#keysplit",
# "midi_mapcc": "http://gareus.org/oss/lv2/midifilter#mapcc",
# "midi_map_key_channel": "http://gareus.org/oss/lv2/midifilter#mapkeychannel",
# "midi_map_key_scale": "http://gareus.org/oss/lv2/midifilter#mapkeyscale",
# "midi_chord": "http://gareus.org/oss/lv2/midifilter#midichord",
# "midi_delay": "http://gareus.org/oss/lv2/midifilter#mididelay",
# "midi_dup": "http://gareus.org/oss/lv2/midifilter#mididup",
# "midi_strum": "http://gareus.org/oss/lv2/midifilter#midistrum",
# "midi_transpose": "http://gareus.org/oss/lv2/midifilter#miditranspose",
# "midi_mono_legato": "http://gareus.org/oss/lv2/midifilter#monolegato",
# "midi_no_active_sensing": "http://gareus.org/oss/lv2/midifilter#noactivesensing",
# "midi_nodup": "http://gareus.org/oss/lv2/midifilter#nodup",
# "midi_note_to_cc": "http://gareus.org/oss/lv2/midifilter#notetocc",
# "midi_note_toggle": "http://gareus.org/oss/lv2/midifilter#notetoggle",
# "midi_note_to_pgm": "http://gareus.org/oss/lv2/midifilter#notetopgm",
# "midi_ntap_delay": "http://gareus.org/oss/lv2/midifilter#ntapdelay",
# "midi_one_channel_filter": "http://gareus.org/oss/lv2/midifilter#onechannelfilter",
# "midi_quantize": "http://gareus.org/oss/lv2/midifilter#quantize",
# "midi_rand_velocity": "http://gareus.org/oss/lv2/midifilter#randvelocity",
# "midi_scale_cc": "http://gareus.org/oss/lv2/midifilter#scalecc",
# "midi_sostenuto": "http://gareus.org/oss/lv2/midifilter#sostenuto",
# "midi_tonal_pedal": "http://gareus.org/oss/lv2/midifilter#tonalpedal",
# "midi_velocity_gamma": "http://gareus.org/oss/lv2/midifilter#velocitygamma",
# "midi_velocity_range": "http://gareus.org/oss/lv2/midifilter#velocityrange",
# "midi_velocity_scale": "http://gareus.org/oss/lv2/midifilter#velocityscale",
# 'matrix_mixer': 'http://gareus.org/oss/lv2/matrixmixer#i4o3',
# "tuner": 'http://gareus.org/oss/lv2/tuna#one',
"clock_divider": 'http://polyeffects.com/lv2/basic_modular#clock_divider',
        }

def parse_ttl(ttl_file, uri, name="placeholder"):
    rdf_dict = RDFdict()
    #we parse the file into the rdf_dict.graph which is a rdflib.ConjunctiveGraph
    rdf_dict.parse(ttl_file, subject=uri)

    #we populate rdf_dict with a structure
    rdf_dict.structure()
    #we replace the Literals with ints, floats and strings and the URIRefs according to the 
    #namespaces we know about
    rdf_dict.interpret(ns.lv2, ns.w3, ns.usefulinc, ns.kxstudio)
    r = rdf_dict[rdflib.term.URIRef(uri)]
    ports = [list(a.values())[0] for a in r["lv2:port"]]
    list(r["lv2:port"][0].values())[0]
    # [a for a in rdf_dict.values() if "lv2:symbol" in a and a["rdf:type"] == ["lv2:ControlPort", "lv2:InputPort"]]
    # {sc["lv2:symbol"][0] : [sc["lv2:name"][0], sc["lv2:default"][0], sc["lv2:minimum"][0], sc["lv2:maximum"][0]]}
    c = [a for a in ports if "lv2:symbol" in a and (set(a["rdf:type"]).issuperset(set(["lv2:ControlPort", "lv2:InputPort"])))] #or
#        set(a["rdf:type"]).issuperset(set(["lv2:CVPort", "lv2:InputPort"])))]
    controls = dict([[sc["lv2:symbol"][0], [sc["lv2:name"][0], sc["lv2:default"][0] if "lv2:default" in sc else 0.5, sc["lv2:minimum"][0] if "lv2:minimum" in sc else 0.0,
        sc["lv2:maximum"][0] if "lv2:maximum" in sc else 1.0]] for sc in c])
        # sc["lv2:maximum"][0] if "lv2:maximum" in sc else 1.0, "int"]] for sc in c])
    i_a = [[a["lv2:symbol"][0], [a["lv2:name"][0], "AudioPort"]] for a in ports if "lv2:symbol" in a and set(a["rdf:type"]).issuperset(set(["lv2:AudioPort",
        "lv2:InputPort"]))]
    i_cv = [[a["lv2:symbol"][0], [a["lv2:name"][0], "CVPort"]] for a in ports if "lv2:symbol" in a and set(a["rdf:type"]).issuperset(set(["lv2:CVPort",
        "lv2:InputPort"]))]
    i_atom = [[a["lv2:symbol"][0], [a["lv2:name"][0], "AtomPort"]] for a in ports if "lv2:symbol" in a and set(a["rdf:type"]).issuperset(set(["atom:AtomPort",
        "lv2:InputPort"]))]
    inputs = dict(i_a + i_cv + i_atom)
    outputs = dict([[a["lv2:symbol"][0], [a["lv2:name"][0], [b for b in a["rdf:type"] if b != "lv2:OutputPort"][0][4:].strip(":")]] for a in ports if "lv2:symbol" in a and "lv2:OutputPort" in
        a["rdf:type"]])
    outputs.pop("latency", "")
    out = {"inputs": inputs,
            "outputs": outputs,
            "controls": controls
            }
    # print("'", name,"':", )
    # pprint(out)
    return out
def convert_all():
    a = {}
    for k, v in effect_type_map.items():
        c = 'lv2info '+v+ ' | grep ttl | grep -v manifest | grep -v modgui'
        file_name = subprocess.Popen(c, stdout=subprocess.PIPE, shell=True).stdout.read()[20:].strip()[7:].decode()
        print (file_name, v, k)
        b = parse_ttl(file_name, v, k)
        a[k] = b
        a[k]["description"] = ''
        a[k]["long_description"] = ''
        a[k]["tags"] = {"utilities"}
        a[k]["category"] = 0
    pprint(a)

if __name__ == "__main__":
    # ttl_file = sys.argv[1] #"/usr/lib/lv2/avw.lv2/lfo_tempo.ttl"
    # uri = rdflib.URIRef(sys.argv[2])
    # out = parse_ttl(ttl_file, uri)
    # pprint(out)
    pprint(effect_type_map)
    convert_all()
