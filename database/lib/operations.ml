let init = 
    let
      full_permissions = 0o777
    in
    Sys.mkdir "db" full_permissions