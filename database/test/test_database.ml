open OUnit2

let empty _ = 
  Database.Operations.init;
  assert_bool "folder db does not exist" (Sys.is_directory "db")

let tests = "test suite for sum" >::: [
  "empty" >:: empty;
]

let _ = run_test_tt_main tests