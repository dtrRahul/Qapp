
<?php

//action.php

$connect = new PDO();

if(isset($_POST[''])){
   $username = $_POST[''];

   $query = "select count(*) as cntUser from auth_user where username='".$username."'";

   $result = pgsql_query($con,$query);
   $response = "<span style='color: green;'>Available.</span>";
   if(pgsql_num_rows($result)){
      $row = pgsql_fetch_array($result);

      $count = $row['cntUser'];

      if($count > 0){
          $response = "<span style='color: red;'>Not Available.</span>";
      }

   }

   echo $response;
   die;
}

?>
