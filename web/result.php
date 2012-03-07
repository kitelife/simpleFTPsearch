<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml2/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en">

<head>
<link rel="stylesheet" href="alice.css" type="text/css" media="screen"/>
</head>
<body>

<h2>Search Result</h2>

<?php
$searchterm=$_POST['searchterm'];
$searchterm=trim($searchterm);

if(!$searchterm)
{
	echo 'You have not entered search details.Please go back and try again.';
	exit;
}

//if(!get_magic_quotes_gpc())
//{
	$searchterm=addslashes($searchterm);
//}
$hostName = 'xxxx';
$userName = 'xxxx';
$passwd = 'xxxx';
$dataBase = 'xxxx';
@ $db=new mysqli($hostName,$userName,$passwd,$dataBase);
//$db->query("SET NAMES 'UTF8'");
if(mysqli_connect_errno())
{
	echo 'Error:Could not connect to database. Please try again later.';
	exit;
}

$query="select * from filelist where fileName like '%".$searchterm."%'";
$result=$db->query($query);

$num_results=$result->num_rows;

echo '<p>Number of File found:'.$num_results.'</p>';

for($i=0;$i<$num_results;$i++)
{
	$row=$result->fetch_assoc();
	$row['articlecontent']=preg_replace("/($searchterm)/i","<font color=red>\\1</font>",$row['articlecontent']);
	
	echo '<div class="applemenu">';
	echo '<div class="silverheader">';
	echo '<A style="cursor:default">';
	echo '<strong>'.($i+1).'.';
	echo htmlspecialchars(stripslashes($row['fileName']));
	echo '</strong>';
	echo '</A>';
	echo '</div>';
	echo '<br />';
	echo 'Path: ';
	echo "<p><font size = '4'>";
	echo '<a href="';
	echo htmlspecialchars(stripslashes($row['Path']));
	echo '" target=_blank>';
	echo htmlspecialchars(stripslashes($row['Path']));
	echo '</a>';
	echo "</font></p>";
	echo '<div class="show">';
	echo 'TimeLastModified: ';
	echo stripslashes($row['lastTimeModified']);
	echo '</div>';
	echo '<br />';
}
$result->free();
$db->close();
?>
</body>
</html>
