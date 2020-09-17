

# This is part of the game ladder v2.0 (ladder2.cgi).
# It deals with the "search" and other functions.
# v2.10 (07/11/2000)





# issue challenge
if(($vbl{'Button'} eq 'Send Challenge') && $vbl{'crname'} && $vbl{'cename'}) {
	if($x=&finduser($vbl{'crname'}, $vbl{'crpw'})) {
		if($y=&finduser($vbl{'cename'})) {
			$mail[0]=$data[$y+$da{'em'}];
			$mail[1]='A Game Challenge';
			$mail[2]="$vbl{'cename'}:\nYou have been challenged to a match by $vbl{'crname'}.\n";
			$mail[2].="Please reply to accept this challenge.";
			$mail[3]=$data[$x+$da{'em'}];
			&mail(@mail);
			$htp=&gethtm('chalsent.htm');
			$tn=&htmfix($vbl{'crname'});
			$tn2=&htmfix($vbl{'cename'});
			$htp=~s/\*msg\*/$tn at $data[$x+$da{'em'}]<br>has challenged<br>$tn2 at $data[$y+$da{'em'}]<br>to a match./;
			print "content-type: text/html\n\n$htp";
			&leave;
		}
	}
	# not found
	&notfound;
}

#---

# search by game name
if(($vbl{'Button'} eq 'Search') && $vbl{'gname'}) {
	@list=undef;
	for($l=0, $x=1; $x < $#data; $x+=$da) {
		$tn=&symcnv($vbl{'gname'});
		if($data[$x+$da{'gn'}] =~ /^$tn$/i) {
			$list[$l]=$x;
			$l++;
		}
	}
	if($list[0]) {
		&show(0, 0, @list);
		&leave;
	}
	# not found
	&notfound;
}

#---

# search by email
if(($vbl{'Button'} eq 'Search') && $vbl{'email'}) {
	@list=undef;
	for($l=0, $x=1; $x < $#data; $x+=$da) {
		if($data[$x+$da{'em'}] =~ /\b$vbl{'email'}\b/i) {
			$list[$l]=$x;
			$l++;
		}
	}
	if($list[0]) {
		&show(0,0, @list);
		&leave;
	}
	# email not found
	&notfound;
}

#---

# search by rank
if(($vbl{'Button'} eq 'Search') && $vbl{'rank'}) {
	if(($vbl{'rank'} > 0) && (($vbl{'rank'}*$da) <= $#data)) {
		&show($vbl{'rank'}, 1);
		&leave;
	}
	# out of bounds
	&notfound;
}

#---

# search by...
if($vbl{'Button'} eq 'Search') {
	# top 10 list
	if($vbl{'select'} eq 'top10') {
		&show(1, 10);
		&leave;
	}
	# top 20 list
	if($vbl{'select'} eq 'top20') {
		&show(1,20);
		&leave;
	}
	# top 50 list
	if($vbl{'select'} eq 'top50') {
		&show(1,50);
		&leave;
	}
	# top 100 list
	if($vbl{'select'} eq 'top100') {
		&show(1,100);
		&leave;
		}
	# bottom 10 list
	if($vbl{'select'} eq 'bot10') {
		&show(-10,10);
		&leave;
	}
	# bottom 20 list
	if($vbl{'select'} eq 'bot20') {
		&show(-20,20);
		&leave;
	}
	# bottom 50 list
	if($vbl{'select'} eq 'bot50') {
		&show(-50,50);
		&leave;
	}
	# bottom 100 list
	if($vbl{'select'} eq 'bot100') {
		&show(-100,100);
		&leave;
	}
}

#---

# change personal info request, send form
if($vbl{'op'} eq 'cpi') {
	$htp=&gethtm('chnginfo.htm');
	print "content-type: text/html\n\n$htp";
	&leave;
}

#---

sub sendpi {
	$htm=&gethtm('chngdat.htm');
	$htm=~s/\*hun\*/&htmfix($vbl{'cn'})/e;
	$htm=~s/\*hpw\*/&htmfix($vbl{'cp'})/e;
	$htm=~s/\*cn\*/&htmfix($vbl{'cn'})/e;
	$htm=~s/\*rn\*/&htmfix($data[$x+$da{'rn'}])/e;
	$htm=~s/\*em\*/$data[$x+$da{'em'}]/;
	$htm=~s/\*age\*/&htmfix($udat[0])/e;
	$htm=~s/("gen_$udat[1]")/$1 CHECKED/;
	($idp, @idd)=split(/ /, $data[$x+$da{'ct'}]);
	$idd=join(' ', @idd);
	$htm=~s/("cprog_$idp")/$1 CHECKED/;
	$htm=~s/\*contact\*/&htmfix($idd)/e;
	$htm=~s/\*skill\*/&htmfix($udat[2])/e;
	$htm=~s/\*ptimes\*/$udat[3]/;
	$htm=~s/\*comm\*/$udat[4]/;
	if($t=$udat[5]) {$t='http://'.$t}
	else {$t='';}
	$htm=~s/\*gurl\*/$t/;
	if($t=$udat[6]) {$t='http://'.$t}
	else {$t='';}
	$htm=~s/\*home\*/$t/;


	unless($t=$udat[5]) {$t=$rurl.'/images/invis.gif';}
	else {$t="http://$t";}
	$htm=~s/\*img\*/$t/;



	print "content-type: text/html\n\n$htm";
}

# from change presonal info form
if($vbl{'op'} eq 'docpi') {
	local($x);
	if($x=&finduser($vbl{'cn'}, $vbl{'cp'})) {
		@udat=split(/\x11/, $data[$x+$da{'ui'}]);
		&sendpi;
		&leave;
	}
	# not found
	&notfound;
}

#--

if($vbl{'op'} eq 'docpid') {
	local($x);
	if($x=&finduser($vbl{'hun'}, $vbl{'hpw'})) {
		@udat=split(/\x11/, $data[$x+$da{'ui'}]);
		$t=&symcnv($vbl{'hun'});

		# game name
		unless($vbl{'cn'}=~/^$t$/i) {
			if(&finduser($vbl{'cn'})) {&sufe(1, "That name is taken");}
			&newgn($x, $vbl{'cn'}, $vbl{'hun'});
		}

		# password
		$t=&symcnv($data[$x+$da{'pw'}]);
		if($vbl{'np'} && ($vbl{'np'}!~/^$t$/i)) {
			# new password
			$t=&symcnv($vbl{'np2'});
			if($vbl{'np'} =~ /^$t$/i) {
				# passwords match
				$data[$x+$da{'pw'}]=$vbl{'np'};
				$vbl{'cp'}=&htmfix($vbl{'np'});
			}
			else{$ackmsg='Password match failed. No change';}
		}
		else {$vbl{'cp'}=$vbl{'hpw'};}

		# real name
		$data[$x+$da{'rn'}]=$vbl{'rn'};
		
		# email
		$data[$x+$da{'em'}]=$vbl{'em'};

		# age
		$udat[0]=$vbl{'age'};

		# gender
		$vbl{'gen'}=~s/gen_(.+)/$1/;
		$udat[1]=$vbl{'gen'};
		
		# contact
		if($t=$vbl{'contact'}) {
			$t=~s/\`/'/g;
			$pt=$vbl{'cprog'};
			$pt=~s/cprog_(.+)/$1/;
			$v=$pt.' '.&bsquote($t);
		}
		else {$v='';}
		$data[$x+$da{'ct'}]=$v;

		# skill
		$udat[2]=&htmfix($vbl{'skill'});

		# times available
		$udat[3]=$vbl{'ptimes'};
		$udat[3]=~s/\xd//g;

		# comments
		$udat[4]=$vbl{'comm'};
		$udat[4]=~s/\xd//g;

		# pic URL
		$udat[5]=$vbl{'gurl'};
		$udat[5]=~s/http:\/\///;
		$udat[5]=$udat[5];

		# home URL
		$udat[6]=$vbl{'home'};
		$udat[6]=~s/http:\/\///;
		$udat[6]=$udat[6];
		
		# end mark
		$udata[7]='-';

		# update data file
		$data[$x+$da{'ui'}]=join("\x11", @udat);
		&uddata;
		&sendpi;
		&leave;
	}
	&sufe(1, "User not found.");
	&leave;
}

#---

# withdraw
if($vbl{'Button'} eq 'Delete Me') {
	$hit=0;
	unless($vbl{'wdgn'} && $vbl{'wdpw'}) {&sufe(0, "Name and password required");}
	if($x=&finduser($vbl{'wdgn'}, $vbl{'wdpw'})) {
		$hit=1;
		$wdgn=&htmfix($vbl{'wdgn'});
		&delmem($x);
		&wrstart;
	}
	unless($hit==1) {
		# user not found
		&notfound;
	}
	&uddata;
	$htp=&gethtm('ackquit.htm');
	$htp=~s/\*msg\*/$wdgn/;
	print "Content-type: text/html\n\n$htp";
	# update member tally
	&leave;
}

#---

if($vbl{'Button'} eq 'Resend Password') {
	if($x=&finduser($vbl{'rsgn'})) {
		# gen email msg
		$emmsg=~s/\*rname\*/$data[$x+$da{'rn'}]/;
		$emmsg=~s/\*name\*/$data[$x+$da{'gn'}]/;
		$emmsg=~s/\*pw\*/$data[$x+$da{'pw'}]/;
		$emmsg=~s/\*act\*/$data[$x+$da{'ac'}]/;
		$emmsg=~s/\*game\*/$game/;
		$emmsg=~s/\*url\*/$rurlpg/;
		$gn=&webfy($data[$x+$da{'gn'}]);
		$pw=&webfy($data[$x+$da{'ac'}]);
		$emmsg=~s/\*online\*/http:\/\/$cgi?login=online&name=$gn&pw=$pw/;
		$emmsg=~s/\*offline\*/http:\/\/$cgi?login=offline&name=$gn&pw=$pw/;
		$mail[0]=$data[$x+$da{'em'}];
		$mail[1]='Ladder Membership';
		$mail[2]=$emmsg;
		&mail(@mail);
		$htp=&gethtm('resent.htm');
		print "Content-type: text/html\n\n$htp";
		&leave;
	}
	&notfound;
}

#---

# about
if($vbl{'op'} eq 'about') {
	$htp=&gethtm('about.htm');
	$htp=~s/\*owner\*/$cfg[13]/;
	$htp=~s/\*pg\*/$cfg[14]/;
	$htp=~s/\*co\*/$agent/;
	$htp=~s/\*script\*/$script/;
	print "Content-type: text/html\n\n$htp";
	&leave;
}

#---

# no match
&spgset;
&leave;

#---

sub spgset {
	$htp=&gethtm('srch.htm');
	$n=$#data/$da;
	$htp=~s/\*members\*/$n/;
	$t=&makeusers;
	$htp=~s/\*mnsel\*/$t/;
	print "content-type: text/html\n\n$htp";
	&leave;
}

#---

sub notfound {
	$htp=&gethtm('incomp.htm');
	print "Content-type: text/html\n\n$htp";
	&leave;
}