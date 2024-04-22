open Cmdliner
open Database

let cmd = Cmd.group (Cmd.info "database")
  [ Cmd.v (Cmd.info "init") (Term.const init) ]



let main = exit (Cmd.eval cmd)

let () = main