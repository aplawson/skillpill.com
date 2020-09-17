#!/usr/bin/perl
# 1) the line above determines where PERL is installed on your server


# 2) Enter the path to the mail program on your webserver
#    NOTE: Path should BEGIN with a "/" and ends the sendmail or blarg mail program
#    The example below assumes you are using sendmail on a *NIX webserver
#
#    Check your server documents to find out where exactly your mail program is
#    I think the mail prog for NT is 'blarg', but you'll want to make sure
$mail='/usr/lib/sendmail -t';


# 3) Enter the URL to the ladder script (in this case, 'engine.cgi')
#    NOTE: Path should BEGIN with "http://" (without the quotes) and
#    end with the name of the ladder script
$cgi='http://www.yourdomain.com/cgi-bin/engine.cgi';


# 4) Enter the absolute path (not the URL) to the directory with the ladder PAGES
#    NOTE: Path should BEGIN with a "/" and end WITHOUT a trailing "/"
$rpath='/system/path/to/your/ladder/directory';


# 5) URL to ladder directory
#    NOTE: Path should BEGIN with "http://" (without the quotes) and
#    end WITHOUT any trailing slash
$rurl='http://www.skillpill.com/ladder';


# 6) URL for your "home" link
#    NOTE: Path should BEGIN with "http://" (without the quotes) and
#    end WITHOUT any trailing slash
$home='http://www.skillpill.com/ladder';


# 7) full url to the directory containing the image directory
#    NOTE: Path should BEGIN with "http://" (without the quotes) and
#    end WITH a trailing slash
$htmimg='http://www.skillpill.com/ladder/images/';

#--------- ABOVE VARIABLES *MUST* BE CONFIGURED ------
#=====================================================
#--------- ABOVE VARIABLES *MAY* BE CONFIGURED -------


# File used for the included java applet which scrolls the top X players on the start.htm page
$topmem='galascr.txt';


# Backup file for the top ten list for the java applet
$topmemb='galascr.bak';


# File used for the top ten list for SSI for placing top 10 members on start page
$topssi='top10ssi.htm';


# Backup file for the Top 10 list when using a text list vs the applet
$topssib='top10ssi.bak';


# This will save a text file which can be used as a SSI include or any other means 
# if you want your pages to have a look similar to MyLeague (it's just an ongoing tally)
# TOTAL NUMBER OF REGISTERED PLAYERS
$tallymem='totalmem.txt';

# name for tally of total members for ssi, backup
$tallymemb='totalmem.bak';

# This will save a text file which can be used as a SSI include or any other means 
# if you want your pages to have a look similar to MyLeague (it's just an ongoing tally)
# TOTAL NUMBER OF MATCHES PLAYED
$tallygames='totalgames.txt';

# No need to fuss with this, but you're free to change them if you want to---
# These just help generate a nice activation code which is formed from the first two characters
# of the user email, followed by a randomly selected name
# from this list, followed by a random number of 4 digits
@pwl=('grog','roar','tig','ram','bullet','axe','beam');

# The Sysop Section always lists all memebrs and 2 extra blank lines by default.
# Change this value of you want more lines available for adding players manually
$numsysblank=12;

# Want a Top Ten? How about a Top 5? Change the value in the below variable
# and set the limit of how many players you want showcased.
$topnum=10;

# When someone is online, choose the name of the image you want (or are using)
# for the image to be used on the ranks page (when the generic online indicator is desired)

$online='online.gif';

# Below is the initial frames page HTML code.
# You will also be able to change the frames code from within the Administrator Section

$index='
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0 Frameset//EN">
<HTML>
<HEAD>
<TITLE>*title*</TITLE>
</HEAD>
*frames*
<NOFRAMES>
<BODY>
<H2 ALIGN="CENTER">Frame capable browser required.</H2>
</BODY>
</NOFRAMES>
</FRAMESET>
</HTML>
';

# url to ladder index page
# Keep the syntax as follows: $rurlpg="$rurl/index.htm"
# Failing to do so will screw over your ladder generation and end the world! :)

$rurlpg="$rurl/index.htm";

#---------------------------


#============= Set the above as needed/desired ===============#
#======================= end setup ===========================#
###############################################################

$lic=1;
$dkey='Greenhorn Ladder Data v2.1';
$dbrevold='v2.0';
$rev='Rev:1 - Greenhorn Ladder';
$agent='<center>Download this script from
<br>www.skillpill.com</center>';
$script='<center>CGI by Skillpill.com</center>';
$tgllim=40;
$slim=360;
%sy=('dk', 0,
     'xx', 1,
     'we', 2,
     'xx', 3,
     'xx', 4,
     'ea', 5,
     'st', 6,
     'ts', 7);
$sy=8;
%da=('gn', 0,
     'em', 1,
     'st', 2,
     'pw', 3,
     'rh', 4,
     'rn', 5,
     'ac', 6,
     'll', 7,
     'ld', 8,
     'tw', 9,
     'tl', 10,
     'sw', 11,
     'sl', 12,
     'hr', 13,
     'ct', 14,
     'ol', 15,
     'ui', 16,
     'xx', 17);
$da=18;
$cgi=~s/http:\/\/(.+)/$1/;
$recgames="$rpath/recent.dat";
$recgback="$rpath/recent.bak";
$tmem="$rpath/$tallymem";
$baktmem="$rpath/$tallymemb";
$tgame="$rpath/$tallygames";
$ftopssi="$rpath/$topssi";
$bakftopssi="$rpath/$topssib";
$topdogs="$rpath/$topmem";
$baktopdogs="$rpath/$topmemb";
$lock="$rpath/lock.txt";
&lockfile;
if(!(-e $tmem) && $tallymem) {
	open(F, ">$tmem") || &error("Can't init $tmem: $!");
	print F 0;
	close F;
}
if(!(-e $tgame) && $tallygames) {
	open(F, ">$tgame") || &error("Can't init $tgame: $!");
	print F 0;
	close F;
}
unless(-e $recgames) {
    open(F, ">$recgames") || &error("Can't init $recgames");
    close F;
}
%vbl=&parse;
@cfg;
$init=0;
$start=0;
unless(-e "$rpath/cfg.dat") {
	$init=1;
	do 'la2c.cgi';
}
if($vbl{'login'} eq 'goconfig') {
	do 'la2c.cgi';
}
if($vbl{'login'} eq 'config') {
	$start=1;
	do 'la2c.cgi';
}
@cfg=&rdcfg('cfg');
unless($cfg[0]=~/$rev/) {
	&error("config file error: $cfg[0]");
	&leave;
}
$imgtlg=$cfg[24]*24*3600;
@data;
@admin;
&getdata;
if((!(-e $topdogs) && $topmem) || (!(-e $ftopssi) && $topssi)) {&settop10;}
if($admin[$sy{'st'}] =~ /\./) {
	unless($vbl{'login'} =~ /\badmin/) {
		$htd=&gethtm('busy.htm');
		$htd=~s/\*cgi\*/$cgi/;
		delete $vbl{'w_timeout'};
		@a=%vbl;
		$do='';
		for($x=0; $x<=$#a; $x+=2) {
			$do.="<input type=\"hidden\" name=\"$a[$x]\" value=\"$a[$x+1]\">\n";
		}
		$htd=~s/\*formdata\*/$do/;
		print "Content-type: text/html\n\n$htd";
		&leave;
	}
}
if($vbl{'login'} eq 'smd') {
	if($x=&finduser($vbl{'name'})) {
		@udat=split(/\x11/, $data[$x+$da{'ui'}]);
		$htm=&gethtm('uprof.htm');
		$tn=&htmfix($data[$x+$da{'gn'}]);
		$htm=~s/\*gn\*/$tn/;
		if($data[$x+$da{'st'}]=~/R/i) {$t='Rank: '.((($x-1)/$da)+1);}
		else {$t='';}
		$htm=~s/\*rank\*/$t/;
		unless($tl=$udat[5]) {$tl=$rurl.'/images/invis.gif';}
		else {$tl="http://$tl";}
		$htm=~s/\*img\*/$tl/;
		unless($t=$udat[6]) {$t='';}
		if($t) {$htm=~s/\*home\*/<a href="http:\/\/$t" target=\"usr\">Home Page of $tn<\/a>/;}
		else {$htm=~s/\*home\*//;}
		$htm=~s/\*rn\*/&htmfix($data[$x+$da{'rn'}])/e;
		$htm=~s/\*age\*/$udat[0]/;
		$htm=~s/\*gen\*/\u$udat[1]/;
		$htm=~s/\*em\*/&htmfix($data[$x+$da{'em'}])/ge;
		$htm=~s/\*ct\*/&htmfix($data[$x+$da{'ct'}])/e;
		$htm=~s/\*skill\*/&htmfix($udat[2])/e;
		$htm=~s/\*tg\*/&htmfix($udat[3])/e;
		$htm=~s/\*com\*/&htmfix($udat[4])/e;
		print "content-type: text/html\n\n$htm";
		&leave;
	}
	&sufe(0, "Can't find user");
	&leave;
}
if($vbl{'login'} eq 'reqjoin') {
	$htp=&gethtm('join.htm');
	if($ENV{'REMOTE_HOST'}) {$rh=$ENV{'REMOTE_HOST'};}
	else {$rh=$ENV{'REMOTE_ADDR'};}
	$htp=~s/\*info\*/$rh/;
	$htp=~s/\*brsr\*/$ENV{'HTTP_USER_AGENT'}/;
	print "Content-type: text/html\n\n$htp";   
	&leave;
}
if($vbl{'login'} eq 'signup') {
	unless($vbl{'name'}) {&sufe(1, "Game Name missing.");}
	unless($vbl{'realname'}) {&sufe(1, "Real Name missing.");}
	unless($vbl{'em'}=~/.+@.+\.(com|mil|net|org|gov|edu|int|\w{2})$/i) {&sufe(1, "Email missing or invalid.");}
	unless($vbl{'pw1'} && $vbl{'pw2'}) {&sufe(1, "Password missing.");}
	if($vbl{'realname'} =~ /[^a-zA-Z ]/) {&sufe(1, "Invalid real name.");}
	if(($cfg[9] eq 'yes') && ($vbl{'name'} =~ /[^a-zA-Z0-9 ]/)) {&sufe(1, "Invalid game name.");}
	$tpw=&symcnv($vbl{'pw2'});
	unless($vbl{'pw1'}=~/^$tpw$/) {&sufe(1, "Password does not match.");}
	if($ENV{'REMOTE_HOST'}) {$remhost=$ENV{'REMOTE_HOST'};}
	else {$remhost=$ENV{'REMOTE_ADDR'};}
	$tv=&symcnv($vbl{'name'});
	for($x=1; $x < $#data; $x += $da) {
		if($data[$x+$da{'gn'}] =~ /^$tv$/i) {&sufe(1, "Sorry, that name is taken");}
		if($vbl{'em'} eq $data[$x+$da{'em'}]) {
			if($data[$x+$da{'st'}] eq 'B') {
				&sufe(0, "Sorry, you have been blocked from the ladder.");
			}
			if(!($cfg[7] eq 'yes')) {
				&sufe(0, "Sorry, one member per email address.");
			}
		}
		if(!($cfg[8] eq 'yes') && ($remhost eq $data[$x+$da{'rh'}])) {
			&sufe(0, "Sorry, only one member per IP.");
		}			
	}
	$x=@data;                            
	$data[$x+$da{'gn'}]=$vbl{'name'};
	$data[$x+$da{'em'}]=$vbl{'em'};
	$data[$x+$da{'st'}]='P';
	$data[$x+$da{'pw'}]=$vbl{'pw1'};
	$data[$x+$da{'rh'}]=$remhost;
	$data[$x+$da{'rn'}]=$vbl{'realname'};
	srand(time()^($$+($$<<15)));
	$data[$x+$da{'ac'}]=sprintf("%.2s", $vbl{'em'}).$pwl[int(($#pwl+1)*rand)].int(10000*rand);
	$data[$x+$da{'ll'}]=0;
	$data[$x+$da{'ld'}]=time;
	$data[$x+$da{'tw'}]=0;
	$data[$x+$da{'tl'}]=0;
	$data[$x+$da{'sw'}]=0;
	$data[$x+$da{'sl'}]=0;
	if($vbl{'contact'}) {
		$t=$vbl{'contact'};
		$t=~s/\`/'/g;
		$data[$x+$da{'ct'}]=$vbl{'cprog'}.' '.&bsquote($t);
	}
	else{$data[$x+$da{'ct'}]='-';}
	$data[$x+$da{'hr'}]='-';
	$data[$x+$da{'ol'}]=0;
	$data[$x+$da{'xx'}]='-';
	&uddata;
	$emmsg=$cfg[26];
	$emmsg=~s/\*rname\*/$vbl{'realname'}/;
	$emmsg=~s/\*name\*/$vbl{'name'}/;
	$emmsg=~s/\*pw\*/$vbl{'pw1'}/;
	$emmsg=~s/\*act\*/$data[$x+$da{'ac'}]/;
	$emmsg=~s/\*url\*/$rurlpg/;
	$tn=&webfy($vbl{'name'});
	$tp=&webfy($data[$x+$da{'ac'}]);
	$emmsg=~s/\*online\*/http:\/\/$cgi?login=online&name=$tn&pw=$tp/;
	$emmsg=~s/\*offline\*/http:\/\/$cgi?login=offline&name=$tn&pw=$tp/;
	$mail[0]=$vbl{'em'};
	$mail[1]='Ladder Membership';
	$mail[2]=$emmsg;
	&mail(@mail);
	if(($admin[$sy{'ea'}] eq 'yes') && $cfg[12]) {
		$mail[0]=$cfg[12];
		$mail[1]='New Ladder Member';
		$mail[2]="Member: $vbl{'realname'}\n$vbl{'em'}\nhas joind the game ladder.";
		&mail(@mail);
	}
	$htp=&gethtm('ackjoin.htm');
	print "Content-type: text/html\n\n$htp";
	&tmem(1);
	&leave;
}
if($vbl{'login'} eq 'reqact') {
	&activate;
	&leave;
}
if($vbl{'login'} eq 'activate') {
	for($x=1; $x < $#data; $x+=$da) {
		$tv=&symcnv($vbl{'act'});
		if($data[$x+$da{'ac'}] =~ /$tv/) {
			unless($data[$x+$da{'st'}] eq 'P') {&sufe(0, "Account previously activated.");}
			$data[$x+$da{'st'}]='A';
			&uddata;
			$htp=&gethtm('welcome.htm');
			$tn=&htmfix($data[$x+$da{'gn'}]);
			$htp=~s/\*name\*/$tn/;
			print "Content-type: text/html\n\n$htp";
			&udrg($data[$x+$da{'gn'}]);
			&leave;
		}
	}
	&sufe(1, "Sorry, cannot activate that key. Maybe a typing error?");
	&leave;
}
if($vbl{'login'} eq 'showladdr') {
	$un=0;
	$lim=1;
	if($r=$vbl{'showrange'}) {
		if($r=~/u/i) {
			$un=1;
			$hit=0;
			$r=1;
			for($x=1; $x<$#data; $x+=$da) {
				if($data[$x+$da{'st'}]=~/a/i) {
					$hit=1;
					$lim=-1;
					last;
				}
				$r++;
			}
			unless($hit) {
				$lim=0;
			}
		}
	}
	else {$r=1;}
	$x=($r-1)*$da+1;
	if($lim>0) {$lim=$cfg[30]*$da+$x;}
	if($lim<0) {$lim=$#data;}
	@list=undef;
	for($y=0; $x<$lim; $x+=$da) {
		if(!($un) && ($data[$x+$da{'st'}]=~/r/i) ||
			$un && ($data[$x+$da{'st'}]=~/a/i)) {
			$list[$y]=$x;
			$y++;
		}
	}
	&show($r, $cfg[30], @list);
	&leave;
}
if($vbl{'login'} eq 'updatelog') {
	$htp=&gethtm('logloss.htm');
	$t=&makeusers;
	$htp=~s/\*mnsel\*/$t/;
	print "Content-type: text/html\n\n$htp";
	&leave;
}
if($vbl{'login'} eq 'logloss') {
	unless($vbl{'wn'}) {&sufe("Winner name missing.");}
	unless($vbl{'ln'}) {&sufe("Winner name missing.");}
	unless($vbl{'pw'}) {&sufe("Password missing.");}
	$tw=&symcnv($vbl{'wn'});
	$tl=&symcnv($vbl{'ln'});
	$tpw=&symcnv($vbl{'pw'});
	if($vbl{'wn'} =~ /^$tl$/) {&sufe(0,"Can't log game with self");}
	for($wl=$ll=0, $f=0, $er=$#data+1, $x=1; $x < $#data; $x+=$da) {
		if($data[$x+$da{'gn'}] =~ /^$tw$/i) {
			$wl=$x;
		}
		if($data[$x+$da{'gn'}] =~ /^$tl$/i) {
			unless($data[$x+$da{'pw'}] =~ /^$tpw$/i) {
				&sufe(1, "Password failed.");
			}
			$ll=$x;
		}
		unless($f) {
			unless($data[$x+$da{'st'}] eq 'R') {
				$f=1;
				$er=$x;
			}
		}
		if($wl && $ll && $f) {last;}
	}
	unless($wl && $ll) {&sufe(0, "Player not found.");}
    
	if(($data[$wl+$da{'st'}] eq 'B') || ($data[$ll+$da{'st'}] eq 'B')) {
		&sufe(0, "Contest with banned player - action cancelled.");
	}
	$data[$ll+$da{'ll'}]=$data[$wl+$da{'gn'}];
	$gtime=time;
	$data[$ll+$da{'sl'}]+=1;
	$data[$ll+$da{'tl'}]+=1;
	$data[$ll+$da{'sw'}]=0;
	$data[$ll+$da{'ld'}]=$gtime;
	$data[$wl+$da{'sw'}]+=1;
	$data[$wl+$da{'tw'}]+=1;
	$data[$wl+$da{'sl'}]=0;
	$data[$wl+$da{'ld'}]=$gtime;
	$vbl{'comment'}=~s/\xd//g;
	$vbl{'comment'}=~s/`/'/g;
	if(length($vbl{'comment'}) > $cfg[18]) {
		$vbl{'comment'}=sprintf("%.$cfg[18]".'s', $vbl{'comment'}).'...(limit)';
	}
	&udrg($data[$wl+$da{'gn'}], $data[$ll+$da{'gn'}], $vbl{'comment'});
	$data[$wl+$da{'st'}]='R';
	$data[$ll+$da{'st'}]='R';
	if($data[$wl+$da{'hr'}] eq '-') {$data[$wl+$da{'hr'}]='x';}
	if($data[$ll+$da{'hr'}] eq '-') {$data[$ll+$da{'hr'}]='x';}
	$mail[0]=$data[$wl+$da{'em'}];
	$mail[1]='Ladder Position';
	$mail[2]="$data[$ll+$da{'gn'}] has logged your win on the game ladder.";
	&mail(@mail);
	if(($er > $wl) || ($er > $ll)) {
		if($wl > $ll) {
			if($cfg[6]==1) {
				&movsl($ll, $wl, $da, *data);
			}
			elsif(($cfg[6]==2) && ($er >= $wl) && ($er > $ll)) {
				$nwp=int(($wl+$ll-2)/(2*$da))*$da+1;
				&movsl($nwp, $wl, $da, *data);
			}
			elsif(($cfg[6]==2) && ($wl > $er)) {
				$nwp=int(($er-$da+$ll)/(2*$da))*$da+1;
				&movsl($nwp, $wl, $da, *data);
			}
		}
		else {
			if($ll > $er) {
				&movsl($er, $ll, $da, *data);
			}
		}
	}
	else {
		if($wl < $ll) {
			&movsl($er, $wl, $da, *data);
			&movsl($er+$da, $ll, $da, *data);
		}
		else {
			&movsl($er, $ll, $da, *data);
			&movsl($er, $wl, $da, *data);
		}
	}
	for($x=1; $x<$#data; $x+=$da) {
		$ra=(($x-1)/$da)+1;
		if(($data[$x+$da{'hr'}] > $ra) || ($data[$x+$da{'hr'}] eq 'x')) {
			$data[$x+$da{'hr'}]=$ra;
		}
	}
	&uddata;
	&settop10;
	&wrstart;
	$htp=&gethtm('ackloss.htm');
	print "Content-type: text/html\n\n$htp";
	&tgame;
	&leave;
}
if($vbl{'login'} eq 'search') {
	do 'la2s.cgi';
}
if($vbl{'login'} eq 'adminreq') {
	$htp=&gethtm('admli.htm');
	$htp=~s/\*stamp\*/&stamp(0, 'g', $slim, $admin[$sy{'ts'}])/e;
	&uddata;
	print "Content-type: text/html\n\n$htp";
	&leave;
}
if($vbl{'login'} eq 'adminli') {
	$ok=0;
	if(&stamp($vbl{'stamp'}, 'd', $slim, $admin[$sy{'ts'}])) {
		&uddata;
		&sufe(0, "Timeout or improper login");
	}
	$tpw=&symcnv($vbl{'pw'});
	if($cfg[17] =~ /^$tpw$/i) {
		$ok=1;
		$admin[$sy{'st'}]=0;
		$admin[$sy{'ts'}]=0;
	}
	if($admin[$sy{'st'}] =~ /\./) {
		&uddata;
		&sufe(0, "Control panel is busy now.");
	}
	unless($ok) {
		if($cfg[15] =~ /^$tpw$/i) {
			$ok=1;
		}
	}
	unless($ok) {&sufe(1, "Password error");}
	$vbl{'stamp'}=&stamp(0, 'g', $slim, $admin[$sy{'st'}]);
	&uddata;
	&sendadmin;
	&leave;
}
if($vbl{'login'} eq 'admin') {
	srand(time()^($$+($$<<15)));
	if(&stamp($vbl{'stamp'}, 'c', $slim, $admin[$sy{'st'}])) {
		&uddata;
		&sufe(0, "Login error or timeout");
	}
	if($vbl{'Button'} =~ /Log Out/i) {
		&stamp($vbl{'stamp'}, 'd', $slim, $admin[$sy{'st'}]);
		&uddata;
		$htp=&gethtm('admdone.htm');
		print "Content-type: text/html\n\n$htp";
		&leave;
	}
	if($vbl{'Button'} =~ /Help/i) {
		$htp=&gethtm('help.htm');
		print "Content-type: text/html\n\n$htp";
		&leave;
	}
	($tfn, $tfv)=split(/_/, $vbl{'emalrt'});
	$admin[$sy{'ea'}]=$tfv;
	if($vbl{'chem'} eq 'yes') {
		$cfg[12]=$vbl{'ema'};
	}
	if($vbl{'chpw'} eq 'yes') {
		$cfg[15]=$vbl{'napw'};
	}
	if($vbl{'udmsg'} eq 'yes') {
		$vbl{'message'}=~s/\xd//g;
		$admin[$sy{'we'}]=$vbl{'message'};
		&wrstart;
	}
	&uddata;
	&wrcfg('cfg', @cfg);
	if($vbl{'brd'} eq 'cstat') {
		$tpw=&symcnv($vbl{'brpw'});
		if($cfg[16] =~ /^$tpw$/) {
			open(F, ">$recgames");
			close F;
			for($x=1; $x<$#data; $x+=$da) {
				if($data[$x+$da{'st'}] =~ /r/i) {$data[$x+$da{'st'}]='A';}
				$data[$x+$da{'ll'}]='-';
				$data[$x+$da{'ld'}]=time;
				$data[$x+$da{'tw'}]=0;
				$data[$x+$da{'tl'}]=0;
				$data[$x+$da{'sw'}]=0;
				$data[$x+$da{'sl'}]=0;
				$data[$x+$da{'hr'}]='-';
			}
			&uddata;
			&settop10;
			&wrstart;
			&sendadmin;
			&leave;
		}
		else{&sufe(1, "Cancelled: bad password");}
	}
	if($vbl{'brd'} eq 'delete') {
		$tpw=&symcnv($vbl{'brpw'});
		if($cfg[16] =~ /^$tpw$/) {
			if($tallymem) {
				open(F, ">$tmem") || &error("Can't init $tmem: $!");
				print F 0;
				close F;
			}
			open(F, ">$recgames");
			close F;
			$#data=0;
			&settop10;
			&wrstart;
			&uddata;
			&sendadmin;
			&leave;
		}
		else{&sufe(1, "Cancelled: bad password");}
	}
	if($vbl{'brd'} eq 'backup') {
		$tpw=&symcnv($vbl{'brpw'});
		if($cfg[16] =~ /^$tpw$/) {
			$data[0]=join("\x11", @admin);
			$data=join("\x10", @data);
			open(F, ">$cfg[29]") || &error("Can't write $cfg[29]; $!");
			print F $data;
			close(F);
			open(F, $recgames) || &error("Can't read $recgames; $!");
			@tmp=<F>;
			close F;
			open(F, ">$recgback") || &error("Can't write $recgback; $!");
			print F @tmp;
			close F;
			if($tallymem) {
				open(F, $tmem) || &error("Can't read $tmem; $!");
				@tmp=<F>;
				close F;
				open(F, ">$baktmem") || &error("Can't write $baktmem; $!");
				print F @tmp;
				close F;
			}
			&sendadmin;
			&leave;
		}
		else{&sufe(1, "Cancelled: bad password");}
	}
	if($vbl{'brd'} eq 'restore') {
		$tpw=&symcnv($vbl{'brpw'});
		if($cfg[16] =~ /^$tpw$/) {
			unless(-e $cfg[29]) {
				&sufe(1, "No backup file has been created yet.");
				&leave;
			}
			open(F, $cfg[29]) || &error("Can't read $cfg[29]; $!");
			@data=<F>;
			close(F);
			$data=join('', @data);
			$data=~s/\n//;
			@data=split(/\x10/, $data);
			&uddata;
			open(F, $recgback) || &error("Can't read $recgback; $!");
			@tmp=<F>;
			close F;
			open(F, ">$recgames") || &error("Can't write $recgames; $!");
			print F @tmp;
			close F;
			if($tallymem) {
				open(F, $baktmem) || &error("Can't read $baktmem; $!");
				@tmp=<F>;
				close F;
				open(F, ">$tmem") || &error("Can't write $tmem; $!");
				print F @tmp;
				close F;
			}
			&settop10;
			&wrstart;
			&sendadmin;
			&leave;
		}
		else{&sufe(1, "Cancelled: bad password");}
	}
	$x=1;
	$hitm=0;
	while($vbl{'lnum-'.$x}) {
		if($vbl{'mod-'.$x}) {
			&setuvar;
			$hitm=1;
		}
		$x++;
	}
	if($hitm) {
		&uddata;
	}
	@list='';
	$lp=0;
	$x=1;
	$hit=0;
	while($vbl{'lnum-'.$x}) {
		if($vbl{'mod-'.$x} && ($vbl{'stat-'.$x} =~ /d/i)) {
			$list[$lp]=(($x-1)*$da)+1;
			$lp++;
			$hit=1;
		}
		$x++;
	}
	if($hit) {
		&delmem(@list);
		&uddata;
		&wrstart;
		&sendadmin;
		&leave;
	}
	$x=1;
	while($vbl{'lnum-'.$x}) {
		if($vbl{'mod-'.$x} && ($t=$vbl{'move-'.$x})) {
			$mvt=(($t-1)*$da)+1;
			$mvf=(($x-1)*$da)+1;
			&movsl($mvt, $mvf, $da, *data);
			last;
		}
		$x++;
	}
	@td='';
	pop @td;
	for($x=1; $x<$#data; $x+=$da) {
		unless($data[$x+$da{'st'}] =~ /r/i) {
			if($data[$x+$da{'st'}]) {
				@t=@data[$x..($x+$da-1)];
				push(@td, @t);
			}
			$data[$x]=0;
		}
	}
	@data=&packup(1, $da, 0, *data);
	push(@data, @td);
	&uddata;
	&settop10;
	&wrstart;
	&sendadmin;
	&leave;
}
if($vbl{'login'} eq 'online') {
	unless($vbl{'name'} && $vbl{'pw'}) {
		&sufe(0, "Invalid input");
		&leave;
	}
	if($x=&finduser($vbl{'name'})) {
		$tpw=&symcnv($vbl{'pw'});
		if(($data[$x+$da{'ac'}] =~ /$tpw/i) || ($data[$x+$da{'pw'}] =~ /$tpw/i)) {
			$data[$x+$da{'ol'}]=1;
			&uddata;
			$htp=&gethtm('online.htm');
			print "Content-type: text/html\n\n$htp";
			&leave;
		}
	}
	&sufe(0, "User not found");
	&leave;
}
if($vbl{'login'} eq 'offline') {
	unless($vbl{'name'} && $vbl{'pw'}) {
		&sufe(0, "Invalid input");
		&leave;
	}
	if($x=&finduser($vbl{'name'})) {
		$tpw=&symcnv($vbl{'pw'});
		if(($data[$x+$da{'ac'}] =~ /$tpw/i) || ($data[$x+$da{'pw'}] =~ /$tpw/i)) {
			$data[$x+$da{'ol'}]=0;
			&uddata;
			$htp=&gethtm('offline.htm');
			print "Content-type: text/html\n\n$htp";
			&leave;
		}
	}
	&sufe(0, "User not found");
	&leave;
}
if($vbl{'login'} eq 'init') {
	$index=~s/\*title\*/$cfg[5]/;
	$index=~s/\*cgi\*/$cgi/g;
	$index=~s/\*frames\*/$cfg[27]/;
	open(F, ">$rpath/index.htm") || &error("Can't write $rpath/index.htm; $!");
	print F $index;
	close F;
	$htd=&gethtm('navtpl.htm');
	$htd=~s/\*home\*/$home/;
	open(F, ">$rpath/nav.htm") || &error("Can't write $rpath/nav.htm; $!");
	print F $htd;
	close F;
	&wrstart;
	print "Location: $rurlpg\n\n";
	&leave;
}
print "Content-type: text/plain\n\nUnknown input=$vbl{'login'}";
&leave;
sub show {
	local($strt, $num, @list)=@_;
	local($y, @lp, $x);
	unless(@list) {
		unless($strt) {$strt=1;}
		else {
			if($strt > 0) {$strt=($strt-1)*$da+1;}
			else {
				$strt=$#data+1+$strt*$da;
				if($strt < 1) {$strt=1;}
			}
		}   
		unless($num) {$num=$#data;}
		else {$num=$num*$da+$strt-1;}
		if($num > $#data) {$num=$#data;}
		@list=undef;
		for($y=0, $x=$strt; $x < $num; $x+=$da) {
			$list[$y]=$x;
			$y++;
		}
	}
	$htp=&gethtm('ladr.htm');
	$rn=0;
	for($x=1; $x<$#data; $x+=$da) {
		if($data[$x+$da{'st'}]=~/r/i) {$rn++;}
	}
	$do='';
	$n=1;
	$t=$rn-$cfg[30];
	while($t>0) {
		$do.='<OPTION VALUE="'.$n.'">'."$n - " . ($n+$cfg[30]-1) . '</OPTION>' . "\n";
		$rn=$t;
		$n+=$cfg[30];
		$t=$rn-$cfg[30];
	}
	if($rn>1) {
		$do.='<OPTION VALUE="'.$n.'">'."$n - " . ($n+$rn-1) . '</OPTION>' . "\n";
	}
	elsif($rn==1) {$do.='<OPTION VALUE="' . $n . '">' . $n . '</OPTION>' . "\n";}
	$do.='<OPTION VALUE="u">Unranked</OPTION>' . "\n";
	$htp=~s/<\/select>/$do<\/SELECT>/i;
	
	print "Content-type: text/html\n\n";
	($htp[0], $htp[1], $htp[2])=&getrow($htp, '*ra*');
	($recnt, %jmgp) = &setrecntmsg(@list);
	$htp[0]=~s/udx="";/$recnt/;
	print $htp[0];
	$gtime=time;
	
	NEXTSHOW: for($x=0; $x <= $#list; $x++) {
		unless(($data[$list[$x]+$da{'st'}] eq 'A') || ($data[$list[$x]+$da{'st'}] eq 'R')) {
			next NEXTSHOW;
		}
		$t=$htp[1];
		if($data[$list[$x]+$da{'st'}] eq 'R') {
			$r=(($list[$x]-1)/$da)+1;
			$t=~s/\*ra\*/$r/;
		}
		else {
			$t=~s/\*ra\*/-/;
		}
		$t=~s/\*um\*/$data[$list[$x]+$da{'em'}]/;
		@udat=split(/\x11/, $data[$list[$x]+$da{'ui'}]);
		unless($tl=$udat[5]) {$tl=$rurl.'/images/invis.gif';}
		else {$tl="http://$tl";}
		$t=~s/\*img\*/$tl/;
		
		$tn=&htmfix($data[$list[$x]+$da{'gn'}]);
		$t=~s/\*name\*/$tn/;
		$t=~s/\*iname\*/&webfy($data[$list[$x]+$da{'gn'}])/e;
		if($data[$list[$x]+$da{'sw'}] >= $cfg[20]) {
			$t=~s/\*rg\*/$cfg[21]/;
		}
		if($data[$list[$x]+$da{'sl'}] >= $cfg[22]) {
			$t=~s/\*rg\*/$cfg[23]/;
		}
		if(($gtime-$data[$list[$x]+$da{'ld'}]) >= $imgtlg) {
			$t=~s/\*rg\*/$cfg[25]/;
		}
		$t=~s/\*rg\*//;
		$t=~s/"(\w+\.(gif|jpg))"/"$htmimg$1"/g;
		if($data[$list[$x]+$da{'ll'}]) {
			$tn=&htmfix($data[$list[$x]+$da{'ll'}]);
			$t=~s/\*last\*/$tn/;
		
		}
		else {$t=~s/\*last\*/-/;}
		$t=~s/\*tw\*/$data[$list[$x]+$da{'tw'}]/g;
		$t=~s/\*tl\*/$data[$list[$x]+$da{'tl'}]/g;
		$t=~s/\*sw\*/$data[$list[$x]+$da{'sw'}]/g;
		$t=~s/\*sl\*/$data[$list[$x]+$da{'sl'}]/g;
		$t=~s/\*hr\*/$data[$list[$x]+$da{'hr'}]/g;
		$tn=$data[$list[$x]+$da{'gn'}];
		$tn=&bsquote($tn);
		$t=~s/udx/ud$jmgp{$tn}/;
		($cmt, @cmi)=split(/ /, $data[$list[$x]+$da{'ct'}]);
		$cmi=join(' ', @cmi);
		$cmi=&webfy($cmi);
		if($cmt=~/ICQ/) {
			$oli="<img src=\"http://online.mirabilis.com/scripts/online.dll?icq=$cmi&img=1\">";
		}
		elsif($cmt=~/Yahoo/) {
			$oli="<img border=0 src=\"http://opi.yahoo.com/online?u=$cmi&m=g&t=2\">";
		}
		elsif($data[$list[$x]+$da{'ol'}] == 1) {$oli="<img src=\"$htmimg$online\">";}
		else{$oli='-';}
		$t=~s/\*ol\*/$oli/;
		print $t;
	}
	print $htp[2];
	return;
}
sub setrecntmsg {
	local(@list)=@_;
	local($dp,@rg,$rg,$do,$u,$up,@jmgp,$x,@gl,$y, $tv);
	open(F, $recgames) || &error("Can't read $recgames; $!");
	@rg=<F>;
	close F;
	$rg=join('', @rg);
	@rg=split(/\x10/, $rg);
	$do='';
	$u=1;
	$up=0;
	$mdf=0;
	DP: for($dp=0; $dp <= $#list; $dp++) {
		for($x=0; $x<$#rg; $x+=2) {
			$trg=&symcnv($rg[$x]);
			if($data[$list[$dp]+$da{'gn'}] =~ /^$trg$/i) {
				$trg=&bsquote($rg[$x]);
				$jmgp[$up]=$trg;
				$jmgp[$up+1]=$u;
				$up+=2;
				$do.="ud$u=".'"'."$trg<br>Contact: $data[$list[$dp]+$da{'ct'}]".'`"+'."\n";
				$u++;
				if($rg[$x+1] eq '-') {
					$do.='"No games logged"'."\n";
				}
				else {
					@gl=split(/\x11/, $rg[$x+1]);
					for($y=0; $y<=$#gl; $y++) {
						if((($y+3)%4) == 0) {$tgl=&bsquote($gl[$y]);}
						else {$tgl=$gl[$y];}
						if((($y+1)%4) == 0) {
							@tgl=undef;
							$tp=0;
							while(length $tgl > $tgllim) {
								$tgl[$tp]=substr($tgl, 0, $tgllim);
								$tgl[$tp]=&bsquote($tgl[$tp]);
								$tgl[$tp]=~s/\n/<br>/g;
								$tgl=substr($tgl, $tgllim);
								$tp++;
							}
							if($tgl[0]) {
								$tgl[$tp]=$tgl;
								$tgl[$tp]=&bsquote($tgl[$tp]);
								$tgl[$tp]=~s/\n/<br>/g;
								$tgl=join("\"+\n  \"", @tgl);
							
							}
							else {
								$tgl=&bsquote($tgl);
								$tgl=~s/\n/<br>/g;
							}
						}
						$do.='"'.$tgl.'`"+'."\n";
					}
				}
				$do.='"";'."\n\n";
				next DP;
			}
		}
		if($data[$list[$dp]+$da{'st'}]=~/(a|r)/i) {
			$rg[$x]=$data[$list[$dp]+$da{'gn'}];
			$rg[$x+1]='-';
			$mdf=1;
			redo;
		}
	}
	if($mdf) {
		$nrg=join("\x10", @rg);
		open(F, ">$recgames") || &error("Can't write $recgames; $!");
		print F $nrg;
		close F;
	}
	return $do, @jmgp;
}
sub udrg {
	local($w, $l, $c)=@_;
	local(@rd,$rd,$x,$wl,$ll,$time,@tmp,$tw,$tl);
	$tw=&symcnv($w);
	$tl=&symcnv($l);
	open(F, $recgames) || &error("Can't read $recgames; $!");
	@rd=<F>;
	close F;
	$rd=join('', @rd);
	@rd=split(/\x10/, $rd);
	if($l) {
		$time=&dmdy(time);
		$time=~s/(\w\w)(\w\w)(\w\w)/$1\/$2\/$3/;
		$wl=$ll=-1;
		for($x=0; $x<$#rd; $x+=2) {
			if($rd[$x] =~ /^$tw$/i) {
				$wl=$x;
			}
			if($rd[$x] =~ /^$tl$/i) {
				$ll=$x;
			}
			if($wl>=0 && $ll>=0) {
				last;
			}
		}
		if($rd[$wl+1] eq '-') {$rd[$wl+1]='';}
		if($rd[$ll+1] eq '-') {$rd[$ll+1]='';}
	
		if($wl<0) {$wl=@rd;}
		$rd[$wl]=$w;
		$rd[$wl+1]="$time\x11$l\x11won\x11-\x11".$rd[$wl+1];
		@tmp=split(/\x11/, $rd[$wl+1]);
		if($#tmp > $cfg[19]*4) {$#tmp=$cfg[19]*4-1;}
		$rd[$wl+1]=join("\x11", @tmp);
	
		if($ll<0) {$ll=@rd;}
		$rd[$ll]=$l;
		$rd[$ll+1]="$time\x11$w\x11lost\x11$c\x11".$rd[$ll+1];
		@tmp=split(/\x11/, $rd[$ll+1]);
		if(($#tmp) > $cfg[19]*4) {$#tmp=$cfg[19]*4-1;}
		$rd[$ll+1]=join("\x11", @tmp);
	}
	else {
		$rd[$#rd+1]=$w;
		$rd[$#rd+1]='-';
	}
	$rd=join("\x10", @rd);
	open(F, ">$recgames") || &error("Can't write $recgames; $!");
	print F $rd;
	close F;
	return;
}
sub setuvar {
	$p=(($x-1)*$da)+1;
	$vbl{'stat-'.$x}=~s/($vbl{'stat-'.$x})/\U$1/;
	unless($vbl{'name-'.$x}) {return;}
	unless($data[$p+$da{'gn'}]) {
		$data[$p+$da{'gn'}]=$vbl{'name-'.$x};
		$data[$p+$da{'ct'}]='-';
		$data[$p+$da{'rh'}]='-';
		&udrg($data[$p+$da{'gn'}]);
	}
	$tnn=&symcnv($vbl{'name-'.$x});
	unless($data[$p+$da{'gn'}] =~ /$tnn/i) {
		&newgn($p, $vbl{'name-'.$x}, $data[$p+$da{'gn'}]);
	}
	$data[$p+$da{'rn'}]=$vbl{'rna-'.$x};
	$data[$p+$da{'pw'}]=$vbl{'pw-'.$x};
	$data[$p+$da{'em'}]=$vbl{'em-'.$x};
	unless($data[$p+$da{'ac'}]) {
		$data[$p+$da{'ac'}]=sprintf("%.2s", $vbl{'em'}).$pwl[int(($#pwl+1)*rand)].int(10000*rand);
		$data[$p+$da{'ld'}]=time;
	}
	if($vbl{'stat-'.$x}) {$data[$p+$da{'st'}]=$vbl{'stat-'.$x};}
	else {$data[$p+$da{'st'}]='A';}
	if($vbl{'tw-'.$x}) {$data[$p+$da{'tw'}]=$vbl{'tw-'.$x};}
	else {$data[$p+$da{'tw'}]=0;}
	if($vbl{'tl-'.$x}) {$data[$p+$da{'tl'}]=$vbl{'tl-'.$x};}
	else {$data[$p+$da{'tl'}]=0;}
	if($vbl{'sw-'.$x}) {$data[$p+$da{'sw'}]=$vbl{'sw-'.$x};}
	else {$data[$p+$da{'sw'}]=0;}
	if($vbl{'sl-'.$x}) {$data[$p+$da{'sl'}]=$vbl{'sl-'.$x};}
	else {$data[$p+$da{'sl'}]=0;}
	if($vbl{'hr-'.$x}) {$data[$p+$da{'hr'}]=$vbl{'hr-'.$x};}
	else{$data[$p+$da{'hr'}]='-';}
	unless($data[$p+$da{'ol'}] =~ /\d/) {$data[$p+$da{'ol'}]=0;}
}
sub sendadmin {
	$htp=&gethtm('admin.htm');
	$htp=~s/\*stamp\*/$vbl{'stamp'}/g;
	$htp=~s/tstart=15/tstart=$cfg[11]/;
	($htp[0], $htp[1], $htp[2])=&getrow($htp, '*na*');
	print "Content-type: text/html\n\n$htp[0]";
	for($y=$x=1; $x<=$#data; $x+=$da) {
		$t=$htp[1];
		$t=~s/\*fpn\*/$y/g;
		$t=~s/\*n\*/$y/;
		$tn=&htmfix($data[$x+$da{'gn'}]);
		$t=~s/\*na\*/$tn/;
		$t=~s/\*rna\*/$data[$x+$da{'rn'}]/;
		$tn=&htmfix($data[$x+$da{'pw'}]);
		$t=~s/\*pw\*/$tn/;
		$t=~s/\*rh\*/$data[$x+$da{'rh'}]/;
		$t=~s/\*em\*/$data[$x+$da{'em'}]/g;
		$t=~s/\*stat\*/$data[$x+$da{'st'}]/;
		$t=~s/\*tw\*/$data[$x+$da{'tw'}]/;
		$t=~s/\*tl\*/$data[$x+$da{'tl'}]/;
		$t=~s/\*sw\*/$data[$x+$da{'sw'}]/;
		$t=~s/\*sl\*/$data[$x+$da{'sl'}]/;
		$t=~s/\*hr\*/$data[$x+$da{'hr'}]/;
		$y++;
		print $t;
	}
	for($x=0; $x < $numsysblank; $x++) {
		$t=$htp[1];
		$t=~s/\*fpn\*/$y/g;
		$t=~s/\*na\*//;
		$t=~s/\*rna\*//;
		$t=~s/\*pw\*//;
		$t=~s/\*rh\*//;
		$t=~s/\*em\*//;
		$t=~s/\*stat\*//;
		$t=~s/\*date\*//;
		$t=~s/\*tw\*//;
		$t=~s/\*tl\*//;
		$t=~s/\*sw\*//;
		$t=~s/\*sl\*//;
		$t=~s/\*hr\*//;
		print $t;
		$y++;
	}
	$htp[2]=~s/("emalrt_$admin[$sy{'ea'}]")/$1 CHECKED/;
	$htp[2]=~s/\*em\*/$cfg[12]/;
	$htp[2]=~s/\*message\*/$admin[$sy{'we'}]/;
	print $htp[2];
	return;
}
sub finduser {
	local($name, $pw)=@_;
	local($x);
	$name=&symcnv($name);
	$pw=&symcnv($pw);
	for($x=1; $x < $#data; $x += $da) {
		if($data[$x+$da{'gn'}] =~ /^$name$/i) {
			if($pw) {
				if($data[$x+$da{'pw'}]=~/^$pw$/i) {
					return $x;
				}
				return 0;
			}
			return $x;
		}
	}
	return 0;
}
sub makeusers {
	local($op, $x, $op);
	$op="<select onchange='setname(this)'>\n";
	$op.="<option>Type or select name</option>\n";
	for($x=1; $x < $#data; $x += $da) {
		$op.="<option>$data[$x+$da{'gn'}]</option>\n";
	}
	$op.="</select>\n";
	return $op;
}
sub activate {
	$htp=&gethtm('activate.htm');
	$htp=~s/\*info\*/$ENV{'REMOTE_HOST'}/;
	$htp=~s/\*brsr\*/$ENV{'HTTP_USER_AGENT'}/;
	print "Content-type: text/html\n\n$htp";
	&leave;
}
sub sufe {
	open(F, "$rpath/formerr.htm") || &error("Can't read $rpath/joinerr.htm $!");
	@htp=<F>;
	close(F);
	$htp=join('', @htp);
	$htp=~s/(src( |\n)?=( |\n)?")(.+\..+)"/$1$htmimg$4"/ig;
	$htp=~s/(background( |\n?)=( |\n)?")(.+\..+)"/$1$htmimg$4"/i;
	$htp=~s/\*error\*/$_[1]/;
	if($_[0]) {$htp=~s/\*msg\*/Click "Back" on your browser and try again/;}
	else {$htp=~s/\*msg\*//;}
	print "Content-type: text/html\n\n$htp";
	&leave;
}
sub gethtm {
	local($htp, @htp);
	open(F, "$rpath/$_[0]") || &error("Can't open $rpath/$_[0] $!");
	@htp=<F>;
	close(F);
	$htp=join('', @htp);
	$htp=~s/"images\/(\w+\.(gif|jpg))"/"$htmimg$1"/gi;
	$htp=~s/\*url\*/$cgi/g;
	return $htp;
}
sub mail {
	local(@mail)=@_;
	open(MAIL, "|$mail") || &error("Can't open send mail: $mail, To: $vbl{'em'} $!");
	print MAIL "To: $mail[0]\n";
	if($mail[3]) {$fm=$mail[3];}
	else {$fm=$cfg[12];}
	print MAIL "From: $fm\n";
	print MAIL "Subject: $mail[1]\n\n";
	print MAIL "$mail[2]\n\n";
	close(MAIL);
}
sub wrstart {
	local($pg, $top);
	if($cfg[10]) {$pg=&gethtm('strttpll.htm');}
	else {$pg=&gethtm('strttpl.htm');}
	if($topssi) {
		$top=&gethtm($topssi);
		$pg=~s/\*topten\*/$top/;
	}
	else {$pg=~s/\*topten\*//;}
	$pg=~s/\*info\*/$admin[$sy{'we'}]/;
	open(F, ">$rpath/start.htm") || &error("Can't write $rpath/start.htm: $!");
	print F $pg;
	close F;
}
sub settop10 {
	@tl='';
	@tls='';
	$tlp=0;
#	$lim=$#data/$da;
	$topnum;
	for($t=1; $t<=$topnum; $t++) {
		$p=(($t-1)*$da)+1;
		if($data[$p+$da{'st'}] =~ /r/i) {
			$tl[$tlp]="$t: $data[$p+$da{'gn'}]";
			$tls[$tlp]=&htmfix("$t: $data[$p+$da{'gn'}]");
			$tlp++;
		}
		else {last;}
	}
	$tl=join("\n", @tl);
	$tl.="\n";
	$tls=join("<br>\n", @tls);
	$tls.="\n";
	if($topmem) {
		open(F, ">$topdogs") || &error("Can't write $topdogs: $!");
		print F $tl;
		close F;
	}
	if($topssi) {
		open(F, ">$ftopssi") || &error("Can't write $topssi: $!");
		print F $tls;
		close F;
	}
}
sub getdata {
	unless(-e $cfg[28]) {
		open(F, ">$cfg[28]") || &error("Can't write $cfg[28] $!");
		$data="$dkey - Lic: $lic\x11-\x11<center>Welcome</center>\x11-\x11-\x11no\x110\x110";
		print F $data;
		close(F);
	}
	
	
	open(F, $cfg[28]) || &error("Can't read $cfg[28] $!");
	@data=<F>;
	close(F);
	$data=join('', @data);
	@data=split(/\x10/, $data);
	@admin=split(/\x11/, $data[0]);
	unless($admin[$sy{'dk'}] =~ /\b$dkey\b/i) {
		unless($admin[$sy{'dk'}] =~ /\b$dbrevold\b/i) {&error("Bad data file");}
		$np=0;
		@nd=undef;
		for($x=1; $x<$#data; $x+=16) {
			@nd[$np..($np+15)]=@data[$x..($x+15)];
			$nd[$np+17]='-';
			$np+=$da;
		}
		$#data=0;
		push(@data, @nd);
		$admin[$sy{'dk'}]=$dkey;
		&uddata;
	}
}
sub uddata {
	$data[0]=join("\x11", @admin);
	$data=join("\x10", @data);
	open(F, ">$cfg[28]") || &error("Can't write $cfg[28] $!");
	print F $data;
	close(F);
	return;
}
sub bsquote {
	local($c)=$_[0];
	$c=~s/\\/\\\\/g;
	$c=~s/"/\\"/g;
	$c=~s/'/\\'/g;
	unless($_[1]) {
		$c=~s/</&lt;/g;
		$c=~s/>/&gt;/g;
	}
	return $c;
}
sub htmfix {
	local($c)=$_[0];
	$c=~s/"/&quot;/g;
	$c=~s/</&lt;/g;
	$c=~s/>/&gt;/g;
	return $c;
}
sub symcnv {
	local($x)=$_[0];
	$x=~s/(\||\$|\(|\)|\[|\/|\\|\@|\^|\*|\+|\?)/\\$1/g;
	return $x;
}
sub webfy {
	local($a)=$_[0];
	$a=~s/%/%25/g;
	$a=~s/([`~!@#\$\^&*()+=\\|[\]{};:'",<>?\-_.\/])/%$1/g;
	$a=~s/([`~!@#\$\^&*()+=\\|[\]{};:'",<>?\-_.\/])/unpack("H*", $1)/eg;
	$a=~s/ /+/g;
	return $a;
}
sub chkan {
    if($_[0] != /\w/){
        return 0;
    }
    return 1;
}
sub tmem {
	open(F, $tmem) || &error("Can't read $tmem: $!");
	$k=<F>;
	close F;
	$k+=$_[0];
	open(F, ">$tmem") || &error("Can't write $tmem: $!");
	print F $k;
	close F;
}
sub tgame {
	open(F, $tgame) || &error("Can't read $tgame: $!");
	$k=<F>;
	close F;
	$k++;
	open(F, ">$tgame") || &error("Can't write $tgame: $!");
	print F $k;
	close F;
}
sub error {
	print "Content-type: text/plain\n\n@_";
	&leave;
}
sub dmdy {
	local($month, $day, $yr, $date, @t);
	@t=gmtime($_[0]);
	$month=sprintf("%02d", ($t[4]+1));
	$day=sprintf("%02d", $t[3]);
	$yr=sprintf("%02d", $t[5]);
	$date=$month.$day.$yr;
	return $date;
}
sub newgn {
	local($x, $nn, $cn)=@_;
	local($tcn,$bcn,$k,@rg,$rg,$y,@gl,$glp,@td,$td);
	$data[$x+$da{'gn'}]=$nn;
	$tcn=&symcnv($cn);
	$bcn=&bsquote($cn, 1);
	for($k=1; $k < $#data; $k+=$da) {
		if($data[$k+$da{'ll'}] =~ /^$tcn$/i) {
			$data[$k+$da{'ll'}]=$nn;
		}
	}
	open(F, $recgames) || &error("Can't read $recgames; $!");
	@rg=<F>;
	close F;
	$rg=join('', @rg);
	@rg=split(/\x10/, $rg);
	for($y=0; $y < $#rg; $y+=2) {
		if($rg[$y] =~ /^$tcn$/i) {
			$rg[$y]=$nn;
		}
		if($rg[$y+1] ne '-') {
			@gl=split(/\x11/, $rg[$y+1]);
			for($glp=0; $glp<$#gl; $glp+=4) {
				if($gl[$glp+1] =~ /^$tcn$/i) {
					$gl[$glp+1]=$nn;
				}
				$gl[$glp+3]=~s/$bcn/$nn/ig;
			}
			$rg[$y+1]=join("\x11", @gl);
		}
	}
	$rg=join("\x10", @rg);
	open(F, ">$recgames") || &error("Can't write $recgames; $!");
	print F $rg;
	close F;
	&settop10;
}
sub delmem {
	local(@dl)=@_;
	local($x, $dlp, $wdgn, @rg, $rg, $rgp, $tgn, @gd, @td, $td, $tdp);
	open(F, $recgames) || &error("Can't read $recgames; $!");
	@rg=<F>;
	$rg=join('', @rg);
	@rg=split(/\x10/, $rg);
	for($dlp=0; $dlp<=$#dl; $dlp++) {
		$wdgn=$data[$dl[$dlp]+$da{'gn'}];
		$data[$dl[$dlp]+$da{'gn'}]=0;
		$tgn=&symcnv($wdgn);
		for($rgp=0; $rgp <= $#rg; $rgp+=2) {
			if($rg[$rgp] =~ /^$tgn$/i) {
				$rg[$rgp]=0;
			}
			else {
				unless($rg[$rgp+1] eq '-') {
					@gd=split(/\x11/, $rg[$rgp+1]);
					for($x=0; $x<$#gd; $x+=4) {
						if($gd[$x+1] =~ /$tgn/i) {
							$gd[$x+1]=0;
						}
					}
					@gd=&packup(0, 4, 1, *gd);
					unless($gd[0]) {$rg[$rgp+1]='-';}
					else {$rg[$rgp+1]=join("\x11", @gd);}
				}
			}	
		}
		&tmem(-1);
	}
	@data=&packup(1, $da, $da{'gn'}, *data);
	
	@rg=&packup(0, 2, 0, *rg);
	$rg=join("\x10", @rg);
	open(F, ">$recgames") || &error("Can't write $recgames; $!");
	print F $rg;
	close F;
	&settop10;
	
	for($x=1; $x<$#data; $x+=$da) {
		if($data[$x+$da{'ll'}] =~ /$tgn/i) {
			$data[$x+$da{'ll'}]='-';
		}
	}
}
sub parse {
    local (@d, @p, $in, $x);
    if ( $ENV{'REQUEST_METHOD'} eq "GET" ) {
        $in = $ENV{'QUERY_STRING'};
    }
    elsif ($ENV{'REQUEST_METHOD'} eq "POST") {
        read(STDIN,$in,$ENV{'CONTENT_LENGTH'});
    }
    else {
        $in=<STDIN>;
        chop($in);
    }
    $in=~tr/+/ /;
    @d=split(/&/, $in);
    for($x=0; $x<($#d+1); $x++) {
        ($p[$x*2], $p[$x*2+1])=split(/=/, $d[$x]);
        $p[$x*2]=~s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/ge;
        $p[$x*2+1]=~s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/ge;
        $p[$x*2+1]=~s/~!/ ~!/g; 
    }
    return @p;
}
sub stamp {
    local($s, $op, $tl)=@_;
    local($x, @sl, $fhit, $time, $u, $ts);
    @sl=split(/\x12/, $_[3]);
    $fhit=1;
    $time=time;
    for($x=1; $x <= $#sl; $x++) {
        ($u, $ts)=split(/\./, $sl[$x]);
        if((($time-$ts)/60) > $tl || !$sl[$x])  {
            $sl[$x]=$sl[$#sl];
            $#sl--;
            if($x <= $#sl) {redo;}
            else {last;}
        }
        if($op eq 'c') {
            if($sl[$x] == $s) {
                $fhit=0;
                next;
            }
        }
        if($op eq 'd') {
            if($sl[$x] == $s) {
                $sl[$x]=$sl[$#sl];
                $#sl--;
                $fhit=0;
                if($x <= $#sl) {redo;}
                else {last;}
            }
        }
    }
    if($op eq 'g') {
        $sl[0]++;
        $sl[0]=sprintf("%.1s", $sl[0]);
        $fhit=$sl[$#sl+1]="$sl[0].$time";
    }
    $_[3]=join("\x12", @sl);
    return $fhit;
}
sub movsl {
    local($to, $fm, $sz, *a)=@_;
    local(@t);
    if($to > $fm) {
        @t=@a[$fm..($fm+$sz-1)];
        @a[$fm..($to-1)]=@a[($fm+$sz)..($to+$sz-1)]
    }
    else {
        @t=@a[$fm..($fm+$sz-1)];
        @a[($to+$sz)..($fm+$sz-1)]=@a[$to..($fm-1)];
    }
    @a[$to..($to+$sz-1)]=@t;
    return;
}
sub getrow {
	local($page, $key)=($_[0], $_[1]);
	local(@locb, $lp, $sl, $p, $p1, $tgt, $x, $top, $op, $end);
	@locb=undef;
	$lp=0;
	$sl=0;
	do {
		$p=index($page, '<tr', $sl);
        $p1=index($page, '<TR', $sl);
        if(($p1>0 && $p>0 && $p1<$p) || ($p<0)){$p=$p1;}
        $sl=$p+3;
        $locb[$lp]=$p;
        $lp++;
	} while ($p>0);
	$#locb--;
	$tgt=index($page, $key);
	for($x=0; $x<=$#locb; $x++) {
		if($locb[$x]>$tgt) {
			last;
		}
	}
	$x--;
	$p=index($page, '</tr', $locb[$x]);
	$p1=index($page, '</TR', $locb[$x]);
	if(($p1>0 && $p>0 && $p1<$p) || ($p<0)){$p=$p1;}
	$top=substr($page, 0, $locb[$x]);
	$op=substr($page, $locb[$x], ($p-$locb[$x]+5));
	$end=substr($page, $p+5);
	return $top, $op, $end;
}
sub packup {
    local($st, $sz, $ke, *d)=@_;
    local($pi, $po, @op);
    @op[0..($st-1)]=@d[0..($st-1)];
    for($po=$pi=$st; $pi<=$#d; $pi+=$sz) {
        if($d[$pi+$ke]) {
            @op[$po..($po+$sz-1)]=@d[$pi..($pi+$sz-1)];
            $po+=$sz;
        }
    }
    return @op;
}
sub getsfile {
	open(F, "$_[0]") || &error("Can't read $_[0]: $!");
	@d=<F>;
	close F;
	$d=join('', @d);
	return $d;
}
sub wrcfg {
	local($f, @d)=@_;
	local($rv, $d);
	$rv=shift(@d);
	$d=join("\x10", @d)."\x10End of file";
	$d=&tranec($rv, $d);
	open(F, ">$rpath/$f.dat") || &error("Can't write $rpath/$f.dat: $!");
	binmode F;
	print F $d;
	close F;
}
sub rdcfg {
	open(F, "$rpath/$_[0].dat") || &error("Can't read $rpath/$_[0].dat: $!");
	binmode F;
	@d=<F>;
	$d=join('', @d);
	($rv, $d)=&trandc($d);
	@d=split(/\x10/, $d);
	unshift(@d, $rv);
	if($d[$#d] eq 'End of file') {
		$#d--;
		return @d;
	}
	&error("Incomplete read error on config file: $_[0].");
	&leave;
}
sub trandc {
	local($a)=$_[0];
	$st=index($a, '/');
	$en=index($a, '*', ($st+1));
	$rv=substr($a, 0, $st);
	$dk=substr($a, ($st+1), ($en-$st-1));
	$dat=substr($a, ($en+1));
	$dat=&cryp($dat, $dk);
	$dk=$a=undef;
	return ($rv, $dat);
}
sub tranec {
	local($rv, $dat)=@_;
	$time=time;
	$dat=&cryp($dat, $time);
	$dat="$rv/$time*$dat";
	return $dat;
}
	
sub cryp {
    local($d, $k)=@_;
    local($x, $n, $p, @d, @k);
    @d=split(//, $d);
    @k=split(//, $k);
    for($x=0; $x<=$#d; $x++) {$d[$x]=unpack("C", $d[$x]);}
    for($x=0; $x<=$#k; $x++) {$k[$x]=unpack("C", $k[$x]);}
    $n=@k;
    $p=0;
    for($x=0; $x<=$#d; $x++) {
        $d[$x]=$d[$x] ^ $k[$p];
        $d[$x]=pack("C", $d[$x]);
        $p++;
        if($p == $n) {$p=0;}
    }
    $d=join('', @d);
    return $d;
}
sub lockfile {
    local($ttime);
    $ttime=time;
    while(-e $lock) {
    	if(time > $ttime+30) {
    		return;
    	}
    }
    open(LOCK, ">$lock") || &error("Can't write $lock");
    close LOCK;
    return;
}
sub leave {
    unlink $lock;
    exit;
}
