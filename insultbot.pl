#!/usr/pkg/bin/perl

use strict;
use warnings;
use POE;
use POE::Component::IRC::State;
use String::Util 'trim';

sub CHANNEL () { "#lug" }

# Open and read all collections of insults
my $insultpath = "insults.txt";
my $pythonpath = "python.txt";
my $shakespath = "shakespeare.txt";
my $fh;
my $pyfh;
my $shakesfh;
open $fh, '<', "$insultpath" or die "Could not open insult file $insultpath, $!\n";
open $pyfh, '<', "$pythonpath" or die "Could not open insult file $pythonpath, $!\n";
open $shakesfh, '<', "$shakespath" or die "Could not open insult file $shakespath, $!\n";
my @insults = <$fh>;
my @shakes = <$shakesfh>;
my @python = <$pyfh>;
close $fh;
close $pyfh;
close $shakesfh;

my ($irc) = POE::Component::IRC::State->spawn();
POE::Session->create(
	inline_states => {
		_start => \&bot_start,
		irc_001 => \&on_connect,	
		irc_public => \&handle_irc,	
		irc_whois => \&on_whois,
	},
);

sub bot_start {
	$irc->yield(register => "all");
	my $nick = 'insultbot';
	$irc->yield(connect => {
			Nick => $nick,
			Username => $nick,
			Ircname => 'Insulting person',
			Server => 'irc.lug.udel.edu',
			Port => '6667',
			UseSSL => '1',
		},
	);
}

sub add_quote {
	open $fh, '>>', "$insultpath" or die "Could not open insult file $insultpath to add a new insult, $!\n";
	chomp($_[0]);
	print $fh "$_[0]\n";
	close $fh;
	open $fh, '<', "$insultpath" or die "Could not open insult file $insultpath, $!\n";
	@insults = <$fh>;
	close $fh;
}

sub on_connect {
	$irc->yield(join => CHANNEL);
}

sub on_whois {
	my ($kernel, $hashref) = @_[KERNEL, ARG0];
	my ($nick, $ident) = @{ $hashref }{ qw(nick identified) };	
	my $time = scalar localtime;
	print "got a whois for $nick at $time";
	$nick;
}

sub handle_irc {
	my ($kernel, $who, $where, $msg) = @_[KERNEL, ARG0, ARG1, ARG2];
	my $nick = (split /!/, $who)[0];
	chomp($nick);
	my $chan = $where->[0];
	my $ts = scalar localtime;
	my $type;
	my $trigger;
	print " [$ts] <$nick:$chan> $msg\n";
	if ((my $type,my $trigger) = $msg =~ /^!insult \.help/) {
		$irc->yield(privmsg => $nick, "Usage: !insult (.help|.shakes|.python|.add) nick");
		$irc->yield(privmsg => $nick, ".help: Show this help text");
		$irc->yield(privmsg => $nick, ".add: Add a new insult to the default list");
		$irc->yield(privmsg => $nick, ".shakes: Shakespearean style insults");
		$irc->yield(privmsg => $nick, ".python: Monty Python insults");
		$irc->yield(privmsg => $nick, ".list (shakes|python): List the insult group you specify, or by default list the default insults");
		$irc->yield(privmsg => $nick, "No arguments: Standard insults");
	}
	elsif (($trigger) = $msg =~ /^!insult \.list( .+)?/) {
		if ($trigger eq " shakes") {
			$irc->yield(privmsg => $nick, "http://delucks.blinkenshell.org/lists/shakespeare.txt");
		}
		elsif ($trigger eq " python") {
			$irc->yield(privmsg => $nick, "http://delucks.blinkenshell.org/lists/python.txt");
		}
		else {
			foreach (@insults) {
				$irc->yield(privmsg => $nick, "$_");
			}
		}
	}
	#elsif (($trigger) = $msg =~ /^!insult \.list( .+)?/) {
	#	my @list;
	#	if ($trigger eq " shakes") {
	#		@list = @shakes;
	#	}
	#	elsif ($trigger eq " python") {
	#		@list = @python;
	#	}
	#	else {
	#		@list = @insults;
	#	}
	#	foreach (@list) {
	#		$irc->yield(privmsg => $nick, "$_");
	#	}
	#}
	elsif (($type, $trigger) = $msg =~ /^!insult (\.python |\.shakes |\.add )?(.+)/) {
		$trigger = trim($trigger);
		if ($trigger eq "me") {
			$trigger = $nick;
		}
		if ($irc->nick_info($trigger)) {
			if ($type eq ".shakes ") {
				$irc->yield(privmsg => CHANNEL, "$trigger: " . $shakes[rand @shakes]);
			}
			elsif ($type eq ".add ") {
				add_quote $trigger;
				$irc->yield(privmsg => CHANNEL, "$nick: insult added");
			}
			elsif ($type eq ".python ") {
				$irc->yield(privmsg => CHANNEL, "$trigger: " . $python[rand @python]);
			}
			else {
				$irc->yield(privmsg => CHANNEL, "$trigger: " . $insults[rand @insults]);
			}
		}
		else {
			$irc->yield(privmsg => CHANNEL, "I can't find $trigger. $nick, " . $insults[rand @insults]);
		}
	}
}

$poe_kernel->run();
