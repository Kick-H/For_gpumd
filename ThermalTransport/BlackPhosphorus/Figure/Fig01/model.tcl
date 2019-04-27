mol load xyz bp.xyz

#display projection perspective
display projection orthographic
#display backgroundgradient    on
color   Display Background white
#color   Display BackgroundTop black
#color   change  rgb blue 0.52941 0.80784 0.92157
#color   Display BackgroundBot iceblue

axes location off
#display rendermode GLSL
display height 2.0
display cachemode set on
display nearclip set 0.500000
display farclip  set 10.000000
display eyesep       0.06000
display focallength  2.000000
display height       3.0
display distance     -2.000000
display depthcue   off
display cuestart   0.500000
display cueend     10.000000
display cuestart   0.500000
display cueend     10.000000
display cuedensity 0.320000
#display cuemode    Exp2
#display shadows on
#display ambientocclusion on
#display aoambient 1.000000
#display aodirect 0.800000
#display dof on
#display dof_fnumber 64.000000
#display dof_focaldist 0.700000
light 2 on
light 3 on

[atomselect top "z>1"] set name P1
[atomselect top "z<1"] set name P2

mol delrep      top 0
mol addrep        top
mol modcolor    0 top ColorID 0
mol modselect   0 top "z<1 and x<13 and y<11.5"
mol modstyle    0 top VDW 0.5 150
mol modmaterial 0 top Opaque

mol addrep        top
mol modcolor    1 top ColorID 1
mol modselect   1 top "z>1 and x<13 and y<11.5"
mol modstyle    1 top VDW 0.5 150
mol modmaterial 1 top Opaque

mol addrep        top
mol modcolor    2 top ColorID 16
mol modselect   2 top "x<13 and y<11.5"
mol modstyle    2 top DynamicBonds 2.6 0.1 100
mol modmaterial 2 top Opaque

display resetview
display height       3.2

render  Tachyon    out.dat
 "/usr/local/lib/vmd/tachyon_LINUXAMD64" -aasamples 12 out.dat -format TARGA -res 600 500 -o ./model1.tga
exec rm out.dat

rotate x by 90
render  Tachyon    out.dat
 "/usr/local/lib/vmd/tachyon_LINUXAMD64" -aasamples 12 out.dat -format TARGA -res 600 500 -o ./model2.tga
exec rm out.dat
