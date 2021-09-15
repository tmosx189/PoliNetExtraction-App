#!/usr/bin/perl

use utf8
###################################################################
# Create graph using "neato" tool
# Takes the following arguments 

###################################################################

## initialization of arguments
$net_file = $ARGV[0]; chomp($net_file);
$color = $ARGV[1]; chomp($color);
$p_width = $ARGV[2]; chomp($p_width);
$thres_file = $ARGV[3]; chomp($thres_file);

$tmp_smatrix = $net_file; if ($tmp_smatrix =~ /\.txt/) { $tmp_smatrix =~ s/\.txt//g; }

## Out files
$dot_file = $tmp_smatrix.".dot";
$ps_file = $tmp_smatrix.".jpg";

%sim_hash = (); ## Hash matrix with normalized similarity scores
%rat_hash = (); ## Hash matrix with ratings

## open net file
open (I,$net_file) || die "can not open network file $net_file";

$label_flag = 0;
$data_flag = 0;
$num_actors = 0;

$r=<I>;
while ($r ne "")
 {
  chomp ($r);

  ## processing to correctly load the file with the sim score matrix
  $r =~ s/^\s+|\s+$//g;
  $r =~ s/\s+/ /g;

  if ($r =~ m/labels\:/) { $label_flag = 1; $r=<I>; }

  if($label_flag == 1) 
  {
    $r =~ s/\s//g;
    @labels = split(/\,+/,$r);

    for($l=0; $l<=$#labels; $l++) { push(@names,uc($labels[$l])); }
    $label_flag = 0; 
  }

  if ($r =~ m/data\:/) { $data_flag = 1; $r=<I>; }

  if( $data_flag == 1)
  {
    @fields = (); @fields = split(/\s+/,$r);
    @scores = ();
    for ($i=0; $i<=$#fields; $i++)
     { 
	$cur_score = $fields[$i]; 
	push(@scores,$cur_score); 
     }

  ## load normalized similarity scores
  for ($j=0; $j<=$#scores; $j++)
   { $key = $num_actors."_".$j; $value = $scores[$j]; $sim_hash{$key} = $value; }

   $num_actors++;
  }
  $r=<I>;
 }
close(I);
#print ("* Checking normalized similarity matrix: End. OK.\n\n");


## load file with thresholds
open(T,$thres_file) || die("can not open file $thres_file with thresholds\n");
$t=<T>;
while ($t ne "")
{ chomp($t); $t =~ s/\s+//; push(@thres,$t); $t=<T>; }
close (T);
## There must be 4 thresholds
if (!($#thres == 3)) { die "There must be 4 thresholds.\n"; }

## Open dot file to write
open (O,">$dot_file") || die "Can not write dot file\n";
print O ("graph G {\n");
print  O ("graph [overlap=scale, splines=true, orientation=90];\n");
print  O ("node [style=filled,color=grey,fontcolor=black, fontname=Helvetica, fontsize=40, height=1, width=1.25 ,id=1];\n");


for ($c1=0; $c1<=($num_actors-1); $c1++)
 {
  for ($c2=($c1+1); $c2<=($num_actors-1); $c2++)
   {
     $this_key = $c1."_".$c2;

     $norm_sim = $sim_hash{$this_key};
     $rating = $norm_sim; 

     $actor1 = $names[$c1]; $actor2 = $names[$c2];
	
     
     if ( !($rating==0) )
     {
	  $round_rat = sprintf("%.2f",$rating);
	  
	  if( $rating >= 1 && $rating < $thres[0])
	  {
		$colorname = "gray84"; $style="";	
		$pen = 3;
          }
	  elsif( $rating >= $thres[0] && $rating < $thres[1])
	  {
		$colorname = "gray71"; $style="";
		$pen = 5;
          }	
	  elsif( $rating >= $thres[1] && $rating < $thres[2])		
	  {
		$colorname = "gray66"; $style="";
		$pen = 7;
          }
	  elsif( $rating >= $thres[2] && $rating < $thres[3] )		
	  {
		$colorname = "gray51"; $style="";
		$pen = 9;
          }
	  elsif( $rating >= $thres[3] && $rating <=3.00)		
	  {
		$colorname = "black"; $style="";
		$pen = 12;
      }
	   if($color eq "gs" && $p_width == 0)
	   { $record = $actor1." -- ".$actor2." "."[color=$colorname penwidth=$pen ];"; }
	   elsif($color eq "gs" && $p_width > 0) { $record = $actor1." -- ".$actor2." "."[color=$colorname penwidth=$p_width ];"; }
	   elsif($color ne "gs" && $p_width > 0){ $record = $actor1." -- ".$actor2." "."[color=black penwidth=$p_width ];"; }
	   else{ $record = $actor1." -- ".$actor2." "."[color=black penwidth=$pen ];"; }
       ## print parameteres in dot file

	if ($rating >= $thres[3])
       	{	print O ($record,"\n"); }
     }
   }
 }
print O ("}\n");
close (O);

## Create visualization in ps format
system ("neato -Tjpg -Gepsilon=.000001 $dot_file -o $ps_file");
print $ps_file,"\n";

#print ("\n*** Visualization created in $ps_file file *** \n");
