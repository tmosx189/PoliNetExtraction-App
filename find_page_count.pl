#!/usr/bin/perl

use utf8; 
use DBI;
#use PDL;
use HTML::Entities;
use LWP::Simple;
use POSIX;
use Term::ANSIColor;


## read the query
$query = $ARGV[0];
$lang = $ARGV[1];
$year = $ARGV[2];


## if the query has AND (it is an AND query)
if($query =~ /AND/) 
{
   $part1_q = ();
   $part2_q = ();
   $query_final = ();
 
   ($a1,$a2) = split(/\_AND\_/,$query);  

   if( $a1 =~ /OR/)
   {
	@lex = split(/\_OR\_/, $a1); 
	
	for($l=0; $l<=$#lex; $l++)
	{ 
	   $lex[$l] =~ s/\_/ /g;
	   if ( $l < $#lex) { $part1_q .= '"'.$lex[$l].'"'." OR "; }
	   else{ $part1_q .= '"'.$lex[$l].'"' }
	}
   }
   else{ $a1 =~ s/\_/ /g; $part1_q .= '"'.$a1.'"'; }

   

   if( $a2 =~ /OR/)
   {
	@lex = split(/\_OR\_/, $a2); 
	
	for($l=0; $l<=$#lex; $l++)
	{ 
	   $lex[$l] =~ s/\_/ /g;
	   if ( $l < $#lex) { $part2_q .= '"'.$lex[$l].'"'." OR "; }
	   else{ $part2_q .= '"'.$lex[$l].'"' }
	}
   }
   else{ $a2 =~ s/\_/ /g; $part2_q .= '"'.$a2.'"'; }


   ## create AND query
   ##$query_final = '('.$part1_q.')'." AND ".'('.$part2_q.')'; 
   $query_final = '('.$part1_q.')'."+%2B+".'('.$part2_q.')'; 
   $query_final = $part1_q."+%2B+".$part2_q; 	
}
else
{
  $query_final = ();  

  if( $query =~ /OR/)
   {
	@lex = split(/\_OR\_/, $query); 
	
	for($l=0; $l<=$#lex; $l++)
	{ 
	   $lex[$l] =~ s/\_/ /g;
	   if ( $l < $#lex) { $query_final .= '"'.$lex[$l].'"'." OR "; }
	   else{ $query_final .= '"'.$lex[$l].'"' }
	}
   }
   else{ $query =~ s/\_/ /g; $query_final .= '"'.$query.'"'; }
}


#if($year =~ /\d+/) {$query_final = $query_final." ".$year}
if($year =~ /\d+/) {$query_final = $query_final."+%2B+".$year}
$counts = get_count($query_final, $lang);
print $counts,"\n";


##------------------------------------------------------------------------------------------------##
## DOWNLOAD A SINGLE COUNT
##------------------------------------------------------------------------------------------------##

sub get_count{
	my $query = $_[0];
	my $lang = $_[1];

	my	($input,$status) = yahoo_query_raw($query,10,1,"all", $lang);
	my $count = -1;
	my $r1 = "";
	my $r2 = "";
	my $r3 = "";
	if ($status == 1){
		($count,$r1,$r2,$r3) = yahoo_parse_page($input);
	}
	return $count;
}

##------------------------------------------------------------------------------------------------##
## PARSE A YAHOO RESULTS PAGE
##------------------------------------------------------------------------------------------------##

sub yahoo_parse_page {
	my $inpage = $_[0];
	my $count = 0;
	my @snippets = ();
	my @titles = ();
	my @urls = ();
	my @raw_snippets = ();
	
	my $snippet = "";
	my $title = "";
	my $url = "";
	
	$count = yahoo_parse_count($inpage);
	
	## grab/split snippets
	@raw_snippets = split(/class="yschttl spt"/,$inpage);
	@raw_snippets = @raw_snippets[1 .. $#raw_snippets];

	print "found $#raw_snippets raw snippets\n";

	foreach $raw_snippet (@raw_snippets){
	#	($url,$title,$snippet,$status) = yahoo_parse_snippet($raw_snippet);
	#	if ($status == 1){
	#		push(@snippets,$snippet);
	#		push(@urls,$url);
	#		push(@titles,$title);
	#	}
	print $raw_snippet
	}
#	return($count,\@urls,\@titles,\@snippets);
	return $count;
}

##------------------------------------------------------------------------------------------------##
## GRAB A SINGLE YAHOO PAGE
##------------------------------------------------------------------------------------------------##

sub yahoo_query_raw{
	my $query = $_[0];
	my $n = $_[1];
	my $offset = $_[2];
	my $search_in = $_[3];			## html or all
	my $lang = $_[4];			## selected language
	
	# options
	my $allow_adult = "r"; 			# r= NO, p=YES
	my $lang = "lang_".$lang;
	my $line = "";

	my $status = 0;
	my @input = ();
	my $output = "";

	# reform query
#	$query = "\"".$query."\"";
#	$query =~ s/ (AND|NEAR) /" $1 "/g;
	$query =~ s/\s+/\+/g;
	
	#my $url = "http://search.yahoo.com/search?n=".$n."&ei=UTF-8&vd=all&vst=0&vf=".$search_in."&vm=".$allow_adult."&fl=1&vl=".$lang."&p=".$query."&pstart=1&b=".$offset;
	my $url = "https://www.google.com/search?q=".$query; 
	print $url."\n";
	my $tmp = get($url);

	print $tmp."\n";
	system("wget -q ".'"'.$url.'"'." -O response.txt");
	
	if (defined($tmp)){
		@input = split(/\n/,$tmp);
		# save to file
		open F1, ">:utf8", "$offset.html";
		foreach (@input){print F1 $_."\n";}
		close(F1);
		if ($#input >= 1){
			## grab all lines that contain snippets
			$output = "";
			foreach $line (@input){
				chomp($line);
				if (($line =~ /class="yschttl spt"/) or ($line =~ /id=\"resultCount\"\>/)){
					$output = $output." ".$line."\n";
				}
			}
			$output = $input[0];
			$status = 1;
		}
		else{
			print "download error - actual size is $#input\n";
		}
	}
	return ($output,$status);
}

##------------------------------------------------------------------------------------------------##
## PARSE THE COUNT OUT OF A PAGE
##------------------------------------------------------------------------------------------------##

sub yahoo_parse_count{
	my $input = $_[0];
	my $count = 0;

	$input2 = `grep -E -o "[0-9\,?]+ results" response.txt`;

	if ($input2 =~ /([0-9\,?]+)/){
		
		$count = $1;
		$count =~ s/\,//g;
	}
	else{
		#print "COUNT not found\n";
	}

	#system("rm response.txt");

	return $count;
}
