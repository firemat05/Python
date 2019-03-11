import os

scale = "Harbour"

categories = {
    "AidsToNavigation":
    [
        ["P","Beacon_Lateral"],
        ["P","Beacon_Safe_Water"],
        ["P","Beacon_Special_Purpose_General"],
        ["P","Buoy_Cardinal"],
        ["P","Buoy_Isolated_Danger"],
        ["P","Buoy_Lateral"],
        ["P","Buoy_Safe_Water"],
        ["P","Buoy_Special_Purpose_General"],
        ["P","Daymark"],
        ["P","Fog_Signal"],
        ["P","Light"],
        ["P","Light_Float"],
        ["P","Radio_Station"],
        ["P","Retro_Reflector"],
        ["P","Radar_Transponder_Beacon"],
        ["P","Topmark"]
    ],
    "Coastline":
    [
        ["P","Shoreline_Construction"],
        ["L","Coastline"],
        ["L","Shoreline_Construction"],
        ["A","Shoreline_Construction"]
    ],
    "CulturalFeatures":
    [
        ["P","Airport_Airfield"],
        ["P","Builtup_Area"],
        ["P","Building_Single"],
        ["P","Control_Point"],
        ["P","Dam"],
        ["P","Fortified_Structure"],
        ["P","Landmark"],
        ["P","Production_Storage_Area"],
        ["P","Pylon_Bridge_Support"],
        ["P","Silo_Tank"],
        ["L","Bridge"],
        ["L","Cable_Overhead"],
        ["L","Conveyor"],
        ["L","Dam"],
        ["L","Fence_Wall"],
        ["L","Pipeline_Overhead"],
        ["L","Railway"],
        ["L","Road"],
        ["L","Runway"]
        ["L","Tunnel"],
        ["A","Airport_Airfield"],
        ["A","Bridge"],
        ["A","Built_Up"],
        ["A","Building_Single"],
        ["A","Conveyor"],
        ["A","Dam"],
        ["A","Fortified_Structure"],
        ["A","Landmark"],
        ["A","Production_Storage"],
        ["A","Pylon_Bridge_Support"],
        ["A","Runway"],
        ["A","Silo_Tank"],
        ["A","Tunnel"]
    ],
    "Dangers":
    [
        ["P","Caution_Area"],
        ["P","Fishing_Facility"],
        ["P","Obstruction"],
        ["P","Underwater_Awash_Rock"],
        ["P","Water_Turbulence"],
        ["P","Wreck"],
        ["L","Fishing_Facility"],
        ["L","Obstruction"],
        ["L","Oil_Barrier"],
        ["L","Water_Turbulence"],
        ["A","Caution"],
        ["A","Fishing_Facility"],
        ["A","Obstruction"],
        ["A","Water_Turbulence"],
        ["A","Wreck"]
    ],
    "Depths":
    [
        ["L","Depth_Area"],
        ["L","Depth_Contour"],
        ["A","Depth"],
        ["A","Dredged"],
        ["A","Swept"],
        ["A","Unsurveyed"]
    ],
    "IceFeatures":
    [
        ["A","Ice"]
    ],
    "MetaData":
    [
        ["A","Accuracy_of_Data"],
        ["A","Coverage"],
        ["A","Compilation_Scale_of_Data"],
        ["A","Nautical_Publication_Information"],
        ["A","Navigational_System_of_Marks"],
        ["A","Quality_of_Data"],
        ["A","Sounding_Datum"],
        ["A","Vertical_Datum_of_Data"]
    ],
    "MilitaryFeatures":
    [
        ["A","Harbor.Military_Practice"],
    ],
    "NaturalFeatures":
    [
        ["P","Land_Area"],
        ["P","Land_Elevation"],
        ["P","Land_Region"],
        ["P","Sea_Area_Named_Water_Area"],
        ["P","Sloping_Ground"],
        ["P","Vegetation"],
        ["P","Waterfall"],
        ["L","Land_Area"],
        ["L","Land_Elevation"],
        ["L","Rapids"],
        ["L","River"],
        ["L","Slope_Topline"],
        ["L","Vegetation"],
        ["L","Waterfall"],
        ["A","Lake"],
        ["A","Land"],
        ["A","Land_Region"],
        ["A","Rapids"],
        ["A","River"],
        ["A","Sea_Area_Named_Water"],
        ["A","Sloping_Ground"],
        ["A","Vegetation"]
    ],
    "OffshoreInstallations":
    [
        ["P","Offshore_Platform"],
        ["P","Pipeline_Submarine_On_Land"],
        ["L","Cable_Submarine"],
        ["L","Cable"],
        ["L","Offshore_Platform"],
        ["L","Offshore_Production"],
        ["L","Pipeline"]
    ],
    "PortsAndServices":
    [
        ["P","Berth"],
        ["P","Coastguard_Station"],
        ["P","Crane"],
        ["P","Distance_Mark"],
        ["P","Gate"],
        ["P","Harbour_Facility"],
        ["P","Hulk"],
        ["P","Mooring_Warping_Facility"],
        ["P","Pilot_Boarding_Place"],
        ["P","Pile"],
        ["P","Rescue_Station"],
        ["P","Signal_Station_Traffic"],
        ["P","Signal_Station_Warning"],
        ["P","Small_Craft_Facility"],
        ["L","Berth"],
        ["L","Canal"],
        ["L","Causeway"],
        ["L","Dyke"],
        ["L","Floating_Dock"],
        ["L","Gate"],
        ["L","Mooring_Warping_Facility"],
        ["A","Berth"],
        ["A","Canal"],
        ["A","Causeway"],
        ["A","Crane"],
        ["A","Dock"],
        ["A","Dry_Dock"],
        ["A","Dyke"],
        ["A","Floating_Dock"],
        ["A","Gate"],
        ["A","Gridiron"],
        ["A","Harbour_Facility"],
        ["A","Hulk"],
        ["A","Lock_Basin"],
        ["A","Mooring_Warping_Facility"],
        ["A","Pilot_Boarding_Place"],
        ["A","Small_Craft_Facility"]
    ],
    "RegulatedAreasAndLimits":
    [
        ["P","Anchorage_Area_point (64)
        ["P","Anchor_Berth_point (65)
        ["P","Dumping_Ground_point (66)
        ["P","Log_Pond_point (67)
        ["P","Marine_Farm_Culture_point (68)
        ["P","Sea_Plane_Landing_Area_point (69)
        ["L","Marine_Farm_Culture_line (124)
        ["A","Anchorage_Area (186)
        ["A","Anchor_Berth_area (187)
        ["A","Administration_Area_Named_area (188)
        ["A","Contiguous_Zone_area (189)
        ["A","Cargo_Transhipment_Area (190)
        ["A","Dumping_Ground_area (191)
        ["A","Exclusive_Economic_Zone_area (192)
        ["A","Fishing_Ground_area (193)
        ["A","Harbour_Area_Administrative_area (194)
        ["A","Log_Pond_area (195)
        ["A","Marine_Farm_Culture_area (196)
        ["A","Restricted_Area_area (197)
        ["A","Sea_Plane_Landing_Area (198)
    ],
    "Seabed":
    [
        Harbor.Seabed_Area_point (71)
        Harbor.Sand_Waves_point (72)
        Harbor.Spring_point (73)
        Harbor.Weed_Kelp_point (74)
        Harbor.Seabed_Area_line (126)
        Harbor.Sand_Waves_line (127)
        Harbor.Seabed_Area (200)
        Harbor.Sand_Waves_area (201)
        Harbor.Weed_Kelp_area (202)
    ],
    "Soundings":
    [
        Harbor.Sounding_point (76)
    ],
    "TidesAndVariations":
    [
        Harbor.Current_Non_Gravitational_point (78)
        Harbor.Local_Magnetic_Anomaly_point (79)
        Harbor.Magnetic_Variation_point (80)
        Harbor.Tideway_line (129)
        Harbor.Local_Magnetic_Anomaly_area (204)
        Harbor.Tideway_area (205)
    ],
    "TracksAndRoutes":
    [
        Harbor.Radio_Calling_In_Point (82)
        Harbor.Ferry_Route_line (131)
        Harbor.Navigation_Line (132)
        Harbor.Recommended_Route_Centerline_line (133)
        Harbor.Recommended_Track_line (134)
        Harbor.Traffice_Separation_Line (135)
        Harbor.Traffice_Separation_Schema_Boundary_line (136)
        Harbor.Deep_Water_Route_Part_area (207)
        Harbor.Fairway_area (208)
        Harbor.Ferry_Route_area (209)
        Harbor.Inshore_Traffic_Zone_area (210)
        Harbor.Precautionary_Area (211)
        Harbor.Recommended_Traffic_Lane_Part_area (212)
        Harbor.Recommended_Track_area (213)
        Harbor.Traffic_Separation_Zone_area (214)
        Harbor.Traffic_Separation_Scheme_Lane_Part_area (215)
        Harbor.Two_Way_Route_Part_area (216)
    ]
}

geometries = {"P":"point","L":"line","A":"area"}

Berthing
    AidsToNavigation
        Beacon_Lateral_point
        Beacon_Special_Purpose_General_point
        Buoy_Lateral_point
        Daymark_point
        Fog_Signal_point
        Light_point
        Retro_Reflector_point





for item in categories["Coastline"]:
    print ("{}{}\\\{}_{}").format(scale,item[0],item[1],geometries[item[0]])

