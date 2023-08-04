import re
from string import Formatter

from .globals import *

class NumericEnum(Enum):
	def __init__(self, names):
		d = {name: i for i, name in enumerate(names)}
		super().__init__(d)

class CustomFormatter(Formatter):
	def convert_field(self, value, conversion):
		if conversion == "x": # escape
			return escape_html(value)
		elif conversion == "t": # date[t]ime
			return format_datetime(value)
		elif conversion == "d": # time[d]elta
			return format_timedelta(value)
		return super().convert_field(value, conversion)

# definition of reply class and types

class Reply():
	def __init__(self, type_, **kwargs):
		self.type = type_
		self.kwargs = kwargs

types = NumericEnum([
	"CUSTOM",
	"SUCCESS",
	"BOOLEAN_CONFIG",

	"CHAT_JOIN",
	"CHAT_LEAVE",
	"USER_IN_CHAT",
	"USER_NOT_IN_CHAT",
	"GIVEN_COOLDOWN",
	"MESSAGE_DELETED",
	"DELETION_QUEUED",
	"PROMOTED_CITIZEN",
	"PROMOTED_PARTISAN",
	"PROMOTED_MOD",
	"PROMOTED_ADMIN",
	"KARMA_THANK_YOU",
	"KARMA_GOOD_NOTIFICATION",
	"KARMA_BAD_NOTIFICATION",
	"TRIPCODE_INFO",
	"TRIPCODE_SET",

	"ERR_COMMAND_DISABLED",
	"ERR_NO_REPLY",
	"ERR_NOT_IN_CACHE",
	"ERR_NO_USER",
	"ERR_NO_USER_BY_ID",
	"ERR_ALREADY_WARNED",
	"ERR_NOT_IN_COOLDOWN",
	"ERR_COOLDOWN",
	"ERR_BLACKLISTED",
	"ERR_ALREADY_VOTED",
	"ERR_VOTE_OWN_MESSAGE",
	"ERR_SPAMMY",
	"ERR_SPAMMY_SIGN",
	"ERR_SIGN_PRIVACY",
	"ERR_INVALID_TRIP_FORMAT",
	"ERR_NO_TRIPCODE",
	"ERR_MEDIA_LIMIT",
	"ERR_NO_MEDIA_ALLOWED",
	"ERR_MEDIA_PERMISSION",

	"NOTIF_BADWORD_VALUE",
	"NOTIF_SET_BADWORD",
	"NOTIF_REMOVE_BADWORD",

	"USER_INFO",
	"USER_INFO_MOD",
	"USER_ID_REFRESH",
	"USER_NEW_ID",
	"USERS_INFO",
	"USERS_INFO_EXTENDED",

	"PROGRAM_VERSION",
	"HELP_MODERATOR",
	"HELP_ADMIN",
])

# formatting of these as user-readable text

def em(s):
	# make commands clickable by excluding them from the formatting
	s = re.sub(r'[^a-z0-9_-]/[A-Za-z]+\b', r'</em>\g<0><em>', s)
	return "<em>" + s + "</em>"

def smiley(n):
	if n <= 0: return ":)"
	elif n == 1: return ":|"
	elif n <= 3: return ":/"
	else: return ":("

format_strs = {
	types.CUSTOM: "{text}",
	types.SUCCESS: "☑",
	types.BOOLEAN_CONFIG: lambda enabled, **_:
		"<b>{description!x}</b>: " + (enabled and "enabled" or "disabled"),

	types.CHAT_JOIN: em("You joined the chat!"),
	types.CHAT_LEAVE: em("You left the chat!"),
	types.USER_IN_CHAT: em("You're already in the chat."),
	types.USER_NOT_IN_CHAT: em("You're not in the chat yet. Use /start to join!"),
	types.GIVEN_COOLDOWN: lambda deleted, **_:
		em( "You've been handed a cooldown of {duration!d} for this message"+
			(deleted and " (message also deleted)" or "") ),
	types.MESSAGE_DELETED:
		em( "Your message has been deleted. No cooldown has been "
			"given this time, but refrain from posting it again." ),
	types.DELETION_QUEUED: em("{count} messages matched, deletion was queued."),
	types.PROMOTED_CITIZEN: em("You have been promoted to citizen.\nYou may now send stickers."),
	types.PROMOTED_PARTISAN: em("You have been promoted to partisan.\nYou may now send media."),
	types.PROMOTED_MOD: em("You've been promoted to moderator, run /modhelp for a list of commands."),
	types.PROMOTED_ADMIN: em("You've been promoted to admin, run /adminhelp for a list of commands."),
	types.KARMA_THANK_YOU: em("Message review received.\nThat user's social credit has been updated accordingly."),
	types.KARMA_GOOD_NOTIFICATION:
		em( "A peer liked  this, your social credit has increased (check /id to see your social credit"+
			" or /toggleCredit to turn these notifications off)" ),
	types.KARMA_BAD_NOTIFICATION:
		em( "A peer disliked this, your social credit has decreased (check /id to see your social credit"+
			" or /toggleCredit to turn these notifications off)" ),
	types.TRIPCODE_INFO: lambda tripcode, **_:
		"<b>tripcode</b>: " + ("<code>{tripcode!x}</code>" if tripcode is not None else "unset"),
	types.TRIPCODE_SET: em("Tripcode set. It will appear as: ") + "<b>{tripname!x}</b> <code>{tripcode!x}</code>",

	types.ERR_COMMAND_DISABLED: em("This command has been disabled."),
	types.ERR_NO_REPLY: em("You need to reply to a message to use this command."),
	types.ERR_NOT_IN_CACHE: em("Message not found in cache... ({id_refresh_interval}h passed or bot was restarted)"),
	types.ERR_NO_USER: em("No user found by that name!"),
	types.ERR_NO_USER_BY_ID: em("No user found by that id! Note that all ids rotate every {id_refresh_interval} hours."),
	types.ERR_COOLDOWN: em("Your cooldown expires at {until!t}"),
	types.ERR_ALREADY_WARNED: em("A warning has already been issued for this message."),
	types.ERR_NOT_IN_COOLDOWN: em("This user is not in a cooldown right now."),
	types.ERR_BLACKLISTED: lambda reason, contact, **_:
		em( "You've been blacklisted" + (reason and " for {reason!x}" or "") )+
		( em("\ncontact:") + " {contact}" if contact else "" ),
	types.ERR_ALREADY_VOTED: em("You have already reviewed this message."),
	types.ERR_VOTE_OWN_MESSAGE: em("You can't inform on your own message."),
	types.ERR_SPAMMY: em("Your message has not been sent. Avoid sending messages too fast, try again later."),
	types.ERR_SPAMMY_SIGN: em("Your message has not been sent. Avoid using /sign too often, try again later."),
	types.ERR_SIGN_PRIVACY: em("Your account privacy settings prevent usage of the sign feature. Enable linked forwards first."),
	types.ERR_INVALID_TRIP_FORMAT:
		em("Given tripcode is not valid, the format is ")+
		"<code>name#pass</code>" + em("."),
	types.ERR_NO_TRIPCODE: em("You don't have a tripcode set."),
	types.ERR_MEDIA_LIMIT: em("You can't send media or forward messages at this time, try again later."),
	types.ERR_NO_MEDIA_ALLOWED: em("You can't send media or forward messages to this bot."),
	types.ERR_MEDIA_PERMISSION:lambda kind, **_: em("You don't have permission to send {kind}."),

	types.NOTIF_BADWORD_VALUE: lambda filtername, badword, replacement, **_: em("{filtername!x} filters:\n'{badword!x}' will be replaced by '{replacement!x}'"),
	types.NOTIF_SET_BADWORD: lambda filtername, badword, replacement, **_: em("{filtername!x} successfully set:\n'{badword!x}' will be replaced by '{replacement!x}'"),
	types.NOTIF_REMOVE_BADWORD: lambda filtername, badword, **_: em("{filtername!x} successfully removed:\n'{badword!x}' is now unfiltered"),

	types.USER_INFO: lambda warnings, cooldown, **_:
		"<b>id</b>: {id}, <b>username</b>: citizen, <b>rank</b>: {rank_i} ({rank})\n"+
		"<b>social credit</b>: +{positiveKarma} | -{negativeKarma} )\n"+
		"<b>warnings</b>: {warnings} " + smiley(warnings)+
		( " (one warning will be removed on {warnExpiry!t})" if warnings > 0 else "" ) + ", "+
		"<b>cooldown</b>: "+
		( cooldown and "yes, until {cooldown!t}" or "no" ) + "\n"+
		"<b>last active</b>: {lastActive!t}",
	types.USER_INFO_MOD: lambda cooldown, **_:
		"<b>id</b>: {id}, <b>username</b>: citizen, <b>rank</b>: n/a, "+
		"<b>combined social credit</b>: {karma}\n"+
		"<b>cooldown</b>: "+
		( cooldown and "yes, until {cooldown!t}" or "no" ),
	types.USER_ID_REFRESH: em("All users have been sent to re-education.\nIdentifies have been refreshed."),
	types.USER_NEW_ID: lambda id, **_:
		em("Your new government generated ID: ") + "<code>{id}</code>",
	types.USERS_INFO: "<b>{count}</b> <i>users</i>",
	types.USERS_INFO_EXTENDED:
		"<b>{active}</b> <i>active</i>, {inactive} <i>inactive and</i> "+
		"{blacklisted} <i>blacklisted users</i> (<i>total</i>: {total})",

	types.PROGRAM_VERSION: "commielounge-ng v{version} ~ https://github.com/solarbearcub/secretlounge-ng",
	types.HELP_MODERATOR:
		"<i>Moderators can use the following commands</i>:\n"+
		"  /modhelp - show this text\n"+
		"  /modsay &lt;message&gt; - send an official moderator message\n"+
		"\n"+
		"<i>Or reply to a message and use</i>:\n"+
		"  /info - get info about the user that sent this message\n"+
		"  /warn - warn the user that sent this message (cooldown)\n"+
		"  /delete - delete a message and warn the user\n"
		"  /remove - delete a message without a cooldown/warning",
	types.HELP_ADMIN:
		"<i>Admins can use the following commands</i>:\n"+
		"  /adminhelp - show this text\n"+
		"  /adminsay &lt;message&gt; - send an official admin message\n"+
		"  /motd &lt;message&gt; - set the welcome message (HTML formatted)\n"+
		"  /uncooldown &lt;id | username&gt; - remove cooldown from an user\n"+
		"  /mod &lt;username&gt; - promote an user to the moderator rank\n"+
		"  /admin &lt;username&gt; - promote an user to the admin rank\n"+
		"  /cleanup - mass delete messages by currently banned users\n"+
		"\n"+
		"<i>Or reply to a message and use</i>:\n"+
		"  /blacklist [reason] - blacklist the user who sent this message",
}

localization = {}

def formatForTelegram(m):
	s = localization.get(m.type)
	if s is None:
		s = format_strs[m.type]
	if type(s).__name__ == "function":
		s = s(**m.kwargs)
	cls = localization.get("_FORMATTER_", CustomFormatter)
	return cls().format(s, **m.kwargs)
