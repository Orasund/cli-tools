open Cmdliner

let init = 
    let
      full_permissions = 0o777
    in
    Sys.mkdir "db" full_permissions

let cmd = Cmd.group (Cmd.info "database")
  [ Cmd.v (Cmd.info "init") (Term.const init) ]



let () = exit (Cmd.eval cmd)