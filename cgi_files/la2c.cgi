# Greenhorn Game Ladder Config Ops Rev: 2a (04/20/00)


if($init) {
	# read initializing config
	@cfg=&rdcfg('cfgs');
	# setup data file names
	srand(time()^($$+($$<<15)));
	$cfg[28]="$rpath/".'db'.int(10000*rand).'.dat';
	$cfg[29]="$rpath/".'db'.int(10000*rand).'.bak';
	$cfg[30]=25;
	$cfg[31]='-';
	# init config file
	&wrcfg('cfg', @cfg);
	&getdata;
	$vbl{'stamp'}=&stamp(0, 'g', $slim, $admin[$sy{'st'}]);
	&sendcfg;
	&uddata;
	&leave;
}

#--

if($start) {
	@cfg=&rdcfg('cfg');
	&getdata;
	$htm=&gethtm('cfgli.htm');
	$htm=~s/\*stamp\*/&stamp(0, 'g', $slim, $admin[$sy{'st'}])/e;
	&uddata;
	print "content-type: text/html\n\n$htm";
	&leave;
}

#--

@cfg=&rdcfg('cfg');
&getdata;
if(&stamp($vbl{'stamp'}, 'c', $slim, $admin[$sy{'st'}])) {
	&sufe(0, "Bad ID.");
	&leave;
}

if($vbl{'op'} eq 'start') {
	$t=&symcnv($vbl{'pw'});
	unless($cfg[17] =~ /^$t$/i) {
		&sufe(0, "Bad password");
		&leave;
	}
	&sendcfg;
	&leave;
}

#--

unless($vbl{'Button'} eq 'Finish') {
	&loadcf;
	&sendcfg;
	&leave;
}

#--

&loadcf;
$admin[$sy{'st'}]=0;
&uddata;
$vbl{'login'}='init';

#----------------------- subs ----------------------------

sub loadcf {
	@cfg=&rdcfg('cfg');
	$cfg[5]=$vbl{'title'};
	($tfn, $tfv)=split(/_/, $vbl{'rankmode'});
	$cfg[6]=$tfv;
	($tfn, $tfv)=split(/_/, $vbl{'multiumail'});
	$cfg[7]=$tfv;
	($tfn, $tfv)=split(/_/, $vbl{'multiip'});
	$cfg[8]=$tfv;
	($tfn, $tfv)=split(/_/, $vbl{'namelim'});
	$cfg[9]=$tfv;
	($tfn, $tfv)=split(/_/, $vbl{'startlist'});
	$cfg[10]=$tfv;
	$cfg[11]=$vbl{'admintime'};
	$cfg[12]=$vbl{'emaddy'};
	$cfg[13]=$vbl{'owner'};
	$cfg[13]=~s/\xd//g;
	$cfg[14]=$vbl{'agent2'};
	$cfg[14]=~s/\xd//g;
	$cfg[15]=$vbl{'pass'};
	$cfg[16]=$vbl{'backup'};
	$cfg[17]=$vbl{'ppass'};
	$cfg[18]=$vbl{'maxcom'};
	$cfg[19]=$vbl{'maxlog'};
	$cfg[20]=$vbl{'imgcsw'};
	$cfg[21]=$vbl{'imgsw'};
	$cfg[22]=$vbl{'imgcsl'};
	$cfg[23]=$vbl{'imgsl'};
	$cfg[24]=$vbl{'tfrozen'};
	$cfg[25]=$vbl{'imgfrz'};
	$cfg[26]=$vbl{'emmsg'};
	$cfg[26]=~s/\xd//g;
	$cfg[27]=$vbl{'indexf'};
	$cfg[27]=~s/\xd//g;
	$cfg[30]=$vbl{'showrange'};
	&wrcfg('cfg', @cfg);
}

sub sendcfg {
	$htm=&gethtm('setup.htm');
	if($init) {$htm=~s/first=0/first=1/;}
	$htm=~s/\*burl\*/$rurl/g;
	$htm=~s/\*stamp\*/$vbl{'stamp'}/;
	$htm=~s/\*title\*/&htmfix($cfg[5])/e;
	$htm=~s/("rankmode_$cfg[6]")/$1 SELECTED/;
	$htm=~s/("multiumail_$cfg[7]")/$1 CHECKED/;
	$htm=~s/("multiip_$cfg[8]")/$1 CHECKED/;
	$htm=~s/("namelim_$cfg[9]")/$1 CHECKED/;
	$htm=~s/("startlist_$cfg[10]")/$1 CHECKED/;
	$htm=~s/\*admintime\*/$cfg[11]/;
	$htm=~s/\*emaddy\*/&htmfix($cfg[12])/e;
	$htm=~s/\*owner\*/&htmfix($cfg[13])/e;
	$htm=~s/\*agent2\*/&htmfix($cfg[14])/e;
	$htm=~s/\*pass\*/&htmfix($cfg[15])/e;
	$htm=~s/\*backup\*/&htmfix($cfg[16])/e;
	$htm=~s/\*ppass\*/&htmfix($cfg[17])/e;
	$htm=~s/\*maxcom\*/$cfg[18]/;
	$htm=~s/\*maxlog\*/$cfg[19]/;
	$htm=~s/\*imgcsw\*/$cfg[20]/;
	$htm=~s/\*imgsw\*/&htmfix($cfg[21])/e;
	$htm=~s/\*imgcsl\*/$cfg[22]/;
	$htm=~s/\*imgsl\*/&htmfix($cfg[23])/e;
	$htm=~s/\*tfrozen\*/$cfg[24]/;
	$htm=~s/\*imgfrz\*/&htmfix($cfg[25])/e;
	$htm=~s/\*emmsg\*/&htmfix($cfg[26])/e;
	$htm=~s/\*indexf\*/&htmfix($cfg[27])/e;
	$htm=~s/\*showrange\*/$cfg[30]/;
	print "content-type: text/html\n\n$htm";
}