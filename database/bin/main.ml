open Cmdliner

let read =
  Term.(
    const Database.Operations.read 
    $ Arg.(value (pos 0 string "" (Arg.info ["key"])) )
  )
     
let write = 
  Term.(
    const Database.Operations.write 
    $ Arg.(value (pos 0 string "" (Arg.info ["key"])) )
    $ Arg.(value (pos 0 string "" (Arg.info ["value"])) )
  )

let cmd = Cmd.group (Cmd.info "database")
  [ Cmd.v (Cmd.info "init") (Term.const Database.Operations.init);
  Cmd.v (Cmd.info "read") read;
  Cmd.v (Cmd.info "write") write ]



let main = exit (Cmd.eval cmd)

let () = main