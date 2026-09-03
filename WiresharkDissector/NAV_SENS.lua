-- Dissector Wireshark generato dal CSV
local p_proto = Proto("gnss_telemetry", "GNSS Telemetry Protocol")

-- Mappe Valore -> Descrizione per le enumerazioni
local sensor_status_valstring = {
    [0] = "LINK_FAIL",
    [1] = "DEGRADED",
    [2] = "OPERATIVE"
}

-- Definizione dei campi
local f_ssm_array          = ProtoField.uint32("gnss.ssm_array", "GNSS_SSM_ARRAY", base.HEX)
local f_latitude           = ProtoField.float("gnss.latitude", "GNSS_LATITUDE (deg)")
local f_longitude          = ProtoField.float("gnss.longitude", "GNSS_LONGITUDE (deg)")
local f_track              = ProtoField.uint32("gnss.track", "GNSS_TRACK (deg)", base.DEC)
local f_altitude           = ProtoField.int32("gnss.altitude", "GNSS_ALTITUDE (m)", base.DEC)
local f_ground_speed       = ProtoField.uint32("gnss.ground_speed", "GNSS_GROUND_SPEED", base.DEC)
local f_sensor_status      = ProtoField.uint8("gnss.sensor_status", "GNSS_SENSOR_STATUS", base.DEC, sensor_status_valstring)
local f_satellites         = ProtoField.uint8("gnss.satellites", "SATELLITES", base.DEC)
local f_opmode             = ProtoField.uint8("gnss.opmode", "GNSS_OPMODE", base.DEC)
local f_spare              = ProtoField.uint16("gnss.spare", "SPARE", base.HEX)
local f_pitch              = ProtoField.float("gnss.pitch", "PITCH (deg)")
local f_roll               = ProtoField.float("gnss.roll", "ROLL (deg)")
local f_mag_heading        = ProtoField.uint32("gnss.mag_heading", "MAG_HEADING (deg)", base.DEC)

p_proto.fields = {
    f_ssm_array, f_latitude, f_longitude, f_track, f_altitude,
    f_ground_speed, f_sensor_status, f_satellites, f_opmode,
    f_spare, f_pitch, f_roll, f_mag_heading
}

-- Funzione di dissezione
function p_proto.dissector(buffer, pinfo, tree)
    local length = buffer:len()
    if length < 44 then return end -- Dimensione minima pacchetto (44 byte)

    pinfo.cols.protocol = "VL NAV_SENS_DATA"

    local subtree = tree:add(p_proto, buffer(0, 44), "Navigation sensors readout")

    -- Estrazione campi in Big-Endian (usa :le_float() o :le_uint() se i dati sono Little-Endian)
    subtree:add(f_ssm_array, buffer(0, 4))
    subtree:add(f_latitude, buffer(4, 4))
    subtree:add(f_longitude, buffer(8, 4))
    subtree:add(f_track, buffer(12, 4))
    subtree:add(f_altitude, buffer(16, 4))
    subtree:add(f_ground_speed, buffer(20, 4))
    subtree:add(f_sensor_status, buffer(24, 1))
    subtree:add(f_satellites, buffer(28, 1))
    subtree:add(f_opmode, buffer(29, 1))
    subtree:add(f_spare, buffer(30, 2))
    subtree:add(f_pitch, buffer(32, 4))
    subtree:add(f_roll, buffer(36, 4))
    subtree:add(f_mag_heading, buffer(40, 4))
end

-- Registrazione sulla porta UDP di destinazione (es. porta 5000)
local udp_port = DissectorTable.get("udp.port")
udp_port:add(35000, p_proto)