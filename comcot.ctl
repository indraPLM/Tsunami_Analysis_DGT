#################################################################
#                                                               #
#      Control file for COMCOT tsunami simulation package       #
#      - Main Configuration File (comcot.ctl)                   #
#                                                               #
#---+----1----+----2----+----3----+----4----+----5----+----6----#
#===============================================:================
# General Parameters for Simulation             : Value Field   |
#===============================================:================
# Job Description: One-line brief description may be added here  
 Total Simulated Duration (Wall clock, seconds) :  7200.000      
 Time Interval for Snapshot Output    (seconds) :    60.0        
 Zmax & Gauge Output  (0-ZMax Z;1-Gauge;2-Both) :    22          
 Start Type (0-Cold start; 1-Hot start)         :     0          
 Resuming Time for Hot Start          (Seconds) :     0.00       
 Minimum WaterDepth offshore           (meters) :     0.00, 0.25       
 Initial Cond. (0:FLT,1:File,2:WM,3:LS,4:FLT+LS):     0          
 Boundary Cond.(0-Open;1-Absorb;2-Wall;3-FACTS) :     1, 0          
 Specify Filename of z Input (for BC=3, FACTS)  :23926h.asc
 Specify Filename of u Input (for BC=3, FACTS)  :23926u.asc
 Specify Filename of v Input (for BC=3, FACTS)  :23926v.asc
#
#===============================================:================
# Parameters for Fault Model (Segment 01)       :Values         |
#===============================================:================
 Number of FLT Planes (use fault_multi.ctl if>1):       1          
 Rupture Start Time(,Uplift Duration)  (seconds):       0.0      
 Faulting Option (0:Model-C; 1:Data; 9:Model-T) :       9        
 Focal Depth                            (meters):   20000.00    
 Length of Fault Plane                  (meters):  169000.00    
 Width of Fault Plane                   (meters):   44394.00    
 Dislocation of Fault Plane             (meters):       7.81    
 Strike Angle (theta)                  (degrees):     290.00    
 Dip  Angle (delta)                    (degrees):      10.00    
 Slip/Rake Angle (lamda)               (degrees):     102.00    
 Origin of Numerical Domain: Latitude  (degrees):     -14.0      
 Origin of Numerical Domain: Longitude (degrees):     103.0     
 Epicenter Location: Latitude          (degrees):     -10.28   
 Epicenter Location: Longitude         (degrees):     107.78   
 File Name of Input Data                        : comcot_slip_57_8_mw9.0.txt 
 Data Format (0-COMCOT;1-MOST;2-XYZ;3-ASC)      :       2        
#
#===============================================:================
#  Parameters for Incident Wave Maker           :Values         |
#===============================================:================
 Wave Type  (1-Solitary; 2-given; 3-focusing)   :       1        
 File Name of Input Data (for Type=2)           :fse.dat
 Incident direction( 1:tp,2:bt,3:lf,4:rt,5:obl) :       2        
 Characteristic Wave Amplitude         (meters) :       0.500    
 Typical Water depth                   (meters) :    2000.000    
#
#===============================================:================
#  Parameters for Landslide / Ground Motion     :Values         |
#===============================================:================
 X_Start of Transient Motion Area               :     119.710     
 X_End of Transient Motion Area                 :     119.890     
 Y_Start of Transient Motion Area               :     -0.910     
 Y_End of Transient Motion Area                 :     -0.600     
 File Name of Shape Input[, format(3-XYZ;4-ASC)]: MULTIPLE
 Option (0-OLD; 1-XYT; 2-LS.Solid; 3-LS.Flow)   :       2        
#
#===============================================:================
# Configurations for all grid layers                             
#===============================================:================
# Parameters for 1st-level grids -- layer 01    :Values         |
#===============================================:================
 Run This Layer ?       (0:Yes,       1:No     ):       0        
 Coordinate System   (0-Spherical, 1-Cartesian) :       0        
 Governing Equations (0-linear,    1-nonlinear) :       0        
 Grid Size       (dx, sph:minutes, Cart:meters) :       1.0      
 Time Step Size                       (seconds) :       2.0      
 Bottom Friction Switch (0-ON;1-OFF;2-ON,Var.n) :       1        
 Manning's n (for Fric.Switch=0), {land, water} :       0.013    
 Output Option?   (0-Z+Hu+Hv; 1-Z Only; 2-NONE) :       1        
 X_start                                        :     102.5       
 X_end                                          :     111.5    
 Y_Start                                        :     -14.5     
 Y_end                                          :      -5.5    
 File Name of Bathymetry Data                   : Pangandaran.asc
 Format  (0-OLD;1-MOST;2-XYZ BP;3-XYZ BN;4-ASC) :       4        
 Grid Identification Number (ID)                :      01        
 Grid Level                                     :       1        
 Parent Grid Layer's ID Number                  :       0        
#
#===============================================:================
#  Parameters for Sub-level grid -- layer 02    :Values         |
#===============================================:================
 Run This Layer ?       (0:Yes,       1:No     ):       1        
 Coordinate System   (0:spherical, 1:cartesian) :       0        
 Governing Equations (0:linear,    1:nonlinear) :       0        
 Bottom Friction Switch (0-ON,1-OFF,2:ON,Var.n) :       1        
 Manning's n (for Fric.Switch=0), {land, water} :       0.013    
 Output Option? (0-Z+Hu+Hv; 1-Z Only; 2-NONE)   :       2        
 GridSize Ratio of Parent Grid to Current Grid  :       3        
 X_start                                        :     106.0     
 X_end                                          :     112.0
 Y_Start                                        :      -9.5
 Y_end                                          :      -6.5
 File Name of Bathymetry Data                   : bathy_jawa.asc
 Format (0-OLD;1-MOST;2-XYZ BP;3-XYZ BN;4-ASC)  :       4        
 Grid Identification Number (ID)                :      02
 Grid Level                                     :       2
 Parent Grid Layer's ID Number                  :      01
#
#===============================================:================
#  Parameters for Sub-level grid -- layer 03    :Values         |
#===============================================:================
 Run This Layer ?       (0:Yes,       1:No     ):       1        
 Coordinate System   (0:spherical, 1:cartesian) :       0        
 Governing Equations (0:linear,    1:nonlinear) :       0        
 Bottom Friction Switch (0-ON,1-OFF,2:ON,Var.n) :       1        
 Manning's n (for Fric.Switch=0), {land, water} :       0.013    
 Output Option? (0-Z+Hu+Hv; 1-Z Only; 2-NONE)   :       2        
 GridSize Ratio of Parent Grid to Current Grid  :       3        
 X_start                                        :     108.0     
 X_end                                          :     110.0
 Y_Start                                        :      -8.4
 Y_end                                          :      -7.2
 File Name of Bathymetry Data                   : bathy_jawa.asc
 Format (0-OLD;1-MOST;2-XYZ BP;3-XYZ BN;4-ASC)  :       4        
 Grid Identification Number (ID)                :      03
 Grid Level                                     :       3
 Parent Grid Layer's ID Number                  :      02
#
#===============================================:================
#  Parameters for Sub-level grid -- layer 04    :Values         |
#===============================================:================
 Run This Layer ?       (0:Yes,       1:No     ):       1        
 Coordinate System   (0:spherical, 1:cartesian) :       0        
 Governing Equations (0:linear,    1:nonlinear) :       0        
 Bottom Friction Switch (0-ON,1-OFF,2:ON,Var.n) :       1        
 Manning's n (for Fric.Switch=0), {land, water} :       0.013    
 Output Option? (0-Z+Hu+Hv; 1-Z Only; 2-NONE)   :       2        
 GridSize Ratio of Parent Grid to Current Grid  :       3        
 X_start                                        :     108.75    
 X_end                                          :     109.50 
 Y_Start                                        :      -7.90
 Y_end                                          :      -7.50 
 File Name of Bathymetry Data                   : bathy_jawa.asc
 Format (0-OLD;1-MOST;2-XYZ BP;3-XYZ BN;4-ASC)  :       4        
 Grid Identification Number (ID)                :      04
 Grid Level                                     :       4
 Parent Grid Layer's ID Number                  :      03
#
#===============================================:================
#  Parameters for Sub-level grid -- layer 05    :Values         |
#===============================================:================
 Run This Layer ?       (0:Yes,       1:No     ):       1       
 Coordinate System   (0:spherical, 1:cartesian) :       0        
 Governing Equations (0:linear,    1:nonlinear) :       1        
 Bottom Friction Switch (0-ON,1-OFF,2:ON,Var.n) :       0        
 Manning's n (for Fric.Switch=0), {land, water} :       0.013    
 Output Option? (0-Z+Hu+Hv; 1-Z Only; 2-NONE)   :       0        
 GridSize Ratio of Parent Grid to Current Grid  :       3        
 X_start                                        :    108.9845     
 X_end                                          :    109.1035
 Y_Start                                        :      -7.7695
 Y_end                                          :      -7.6470
 File Name of Bathymetry Data                   : topo_bathy_cilacap.asc
 Format (0-OLD;1-MOST;2-XYZ BP;3-XYZ BN;4-ASC)  :       4        
 Grid Identification Number (ID)                :      05
 Grid Level                                     :       5
 Parent Grid Layer's ID Number                  :      04
#
#===============================================:================
#  Parameters for Sub-level grid -- layer 06    :Values         |
#===============================================:================
 Run This Layer ?       (0:Yes,       1:No     ):       1        
 Coordinate System   (0:spherical, 1:cartesian) :       0        
 Governing Equations (0:linear,    1:nonlinear) :       0        
 Bottom Friction Switch (0-ON,1-OFF,2:ON,Var.n) :       1        
 Manning's n (for Fric.Switch=0), {land, water} :       0.013    
 Output Option? (0-Z+Hu+Hv; 1-Z Only; 2-NONE)   :       2        
 GridSize Ratio of Parent Grid to Current Grid  :       2        
 X_start                                        :    169.1211
 X_end                                          :    182.6549
 Y_Start                                        :    -45.9109
 Y_end                                          :    -35.9596
 File Name of Bathymetry Data                   :grid01_updated.xyz
 Format (0-OLD;1-MOST;2-XYZ BP;3-XYZ BN;4-ASC)  :       3        
 Grid Identification Number (ID)                :      06
 Grid Level                                     :      06
 Parent Grid Layer's ID Number                  :      05
#
#===============================================:================
#  Parameters for Sub-level grid -- layer 07    :Values         |
#===============================================:================
 Run This Layer ?       (0:Yes,       1:No     ):       1        
 Coordinate System   (0:spherical, 1:cartesian) :       0        
 Governing Equations (0:linear,    1:nonlinear) :       0        
 Bottom Friction Switch (0-ON,1-OFF,2:ON,Var.n) :       1        
 Manning's n (for Fric.Switch=0), {land, water} :       0.013    
 Output Option? (0-Z+Hu+Hv; 1-Z Only; 2-NONE)   :       2        
 GridSize Ratio of Parent Grid to Current Grid  :       2        
 X_start                                        :    169.7978
 X_end                                          :    182.0121
 Y_Start                                        :    -45.4134
 Y_end                                          :    -36.4323
 File Name of Bathymetry Data                   :grid01_updated.xyz
 Format (0-OLD;1-MOST;2-XYZ BP;3-XYZ BN;4-ASC)  :       3        
 Grid Identification Number (ID)                :      07
 Grid Level                                     :      07
 Parent Grid Layer's ID Number                  :      06
#
#===============================================:================
#  Parameters for Sub-level grid -- layer 08    :Values         |
#===============================================:================
 Run This Layer ?       (0:Yes,       1:No     ):       1        
 Coordinate System   (0:spherical, 1:cartesian) :       0        
 Governing Equations (0:linear,    1:nonlinear) :       0        
 Bottom Friction Switch (0-ON,1-OFF,2:ON,Var.n) :       1        
 Manning's n (for Fric.Switch=0), {land, water} :       0.013    
 Output Option? (0-Z+Hu+Hv; 1-Z Only; 2-NONE)   :       2        
 GridSize Ratio of Parent Grid to Current Grid  :       2        
 X_start                                        :    170.4085
 X_end                                          :    181.4319
 Y_Start                                        :    -44.9643
 Y_end                                          :    -36.8589
 File Name of Bathymetry Data                   :grid01_updated.xyz
 Format (0-OLD;1-MOST;2-XYZ BP;3-XYZ BN;4-ASC)  :       3        
 Grid Identification Number (ID)                :      08
 Grid Level                                     :      08
 Parent Grid Layer's ID Number                  :      07
#
#===============================================:================
#  Parameters for Sub-level grid -- layer 09    :Values         |
#===============================================:================
 Run This Layer ?       (0:Yes,       1:No     ):       1        
 Coordinate System   (0:spherical, 1:cartesian) :       0        
 Governing Equations (0:linear,    1:nonlinear) :       0        
 Bottom Friction Switch (0-ON,1-OFF,2:ON,Var.n) :       1        
 Manning's n (for Fric.Switch=0), {land, water} :       0.013    
 Output Option? (0-Z+Hu+Hv; 1-Z Only; 2-NONE)   :       2        
 GridSize Ratio of Parent Grid to Current Grid  :       2        
 X_start                                        :    170.9597
 X_end                                          :    180.9083
 Y_Start                                        :    -44.5590
 Y_end                                          :    -37.2439
 File Name of Bathymetry Data                   :grid01_updated.xyz
 Format (0-OLD;1-MOST;2-XYZ BP;3-XYZ BN;4-ASC)  :       3        
 Grid Identification Number (ID)                :      09
 Grid Level                                     :      09
 Parent Grid Layer's ID Number                  :      08
#
#===============================================:================
#  Parameters for Sub-level grid -- layer 10    :Values         |
#===============================================:================
 Run This Layer ?       (0:Yes,       1:No     ):       1        
 Coordinate System   (0:spherical, 1:cartesian) :       0        
 Governing Equations (0:linear,    1:nonlinear) :       0        
 Bottom Friction Switch (0-ON,1-OFF,2:ON,Var.n) :       1        
 Manning's n (for Fric.Switch=0), {land, water} :       0.013    
 Output Option? (0-Z+Hu+Hv; 1-Z Only; 2-NONE)   :       2        
 GridSize Ratio of Parent Grid to Current Grid  :       2        
 X_start                                        :    171.4571
 X_end                                          :    180.4357
 Y_Start                                        :    -44.1933
 Y_end                                          :    -37.5914
 File Name of Bathymetry Data                   :grid01_updated.xyz
 Format (0-OLD;1-MOST;2-XYZ BP;3-XYZ BN;4-ASC)  :       3        
 Grid Identification Number (ID)                :      10
 Grid Level                                     :      10
 Parent Grid Layer's ID Number                  :      09
#
#===============================================:================
#  Parameters for Sub-level grid -- layer 11    :Values         |
#===============================================:================
 Run This Layer ?       (0:Yes,       1:No     ):       1        
 Coordinate System   (0:spherical, 1:cartesian) :       0        
 Governing Equations (0:linear,    1:nonlinear) :       0        
 Bottom Friction Switch (0-ON,1-OFF,2:ON,Var.n) :       1        
 Manning's n (for Fric.Switch=0), {land, water} :       0.013    
 Output Option? (0-Z+Hu+Hv; 1-Z Only; 2-NONE)   :       2        
 GridSize Ratio of Parent Grid to Current Grid  :       2        
 X_start                                        :    171.9061
 X_end                                          :    180.0092
 Y_Start                                        :    -43.8632
 Y_end                                          :    -37.9050
 File Name of Bathymetry Data                   :grid01_updated.xyz
 Format (0-OLD;1-MOST;2-XYZ BP;3-XYZ BN;4-ASC)  :       3        
 Grid Identification Number (ID)                :      11
 Grid Level                                     :      11
 Parent Grid Layer's ID Number                  :      10
#
#===============================================:================
#  Parameters for Sub-level grid -- layer 12    :Values         |
#===============================================:================
 Run This Layer ?       (0:Yes,       1:No     ):       1        
 Coordinate System   (0:spherical, 1:cartesian) :       0        
 Governing Equations (0:linear,    1:nonlinear) :       0        
 Bottom Friction Switch (0-ON,1-OFF,2:ON,Var.n) :       1        
 Manning's n (for Fric.Switch=0), {land, water} :       0.013    
 Output Option? (0-Z+Hu+Hv; 1-Z Only; 2-NONE)   :       2        
 GridSize Ratio of Parent Grid to Current Grid  :       2        
 X_start                                        :    172.3112
 X_end                                          :    179.6243
 Y_Start                                        :    -43.5653
 Y_end                                          :    -38.1880
 File Name of Bathymetry Data                   :grid01_updated.xyz
 Format (0-OLD;1-MOST;2-XYZ BP;3-XYZ BN;4-ASC)  :       3        
 Grid Identification Number (ID)                :      12
 Grid Level                                     :      12
 Parent Grid Layer's ID Number                  :      11
#
#===============================================:================
#  Parameters for Sub-level grid -- layer 13    :Values         |
#===============================================:================
 Run This Layer ?       (0:Yes,       1:No     ):       1        
 Coordinate System   (0:spherical, 1:cartesian) :       0        
 Governing Equations (0:linear,    1:nonlinear) :       0        
 Bottom Friction Switch (0-ON,1-OFF,2:ON,Var.n) :       1        
 Manning's n (for Fric.Switch=0), {land, water} :       0.013    
 Output Option? (0-Z+Hu+Hv; 1-Z Only; 2-NONE)   :       2        
 GridSize Ratio of Parent Grid to Current Grid  :       2        
 X_start                                        :    172.6769
 X_end                                          :    179.2770
 Y_Start                                        :    -43.2964
 Y_end                                          :    -38.4434
 File Name of Bathymetry Data                   :grid01_updated.xyz
 Format (0-OLD;1-MOST;2-XYZ BP;3-XYZ BN;4-ASC)  :       3        
 Grid Identification Number (ID)                :      13
 Grid Level                                     :      13
 Parent Grid Layer's ID Number                  :      12
#
