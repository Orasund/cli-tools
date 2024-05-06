
module StringCompare = struct
  type t = string
  let compare = String.compare
end

module StringMap = Map.Make(StringCompare)
let init = 
  let
    full_permissions = 0o777
  in
  Sys.mkdir "db" full_permissions

let parse string =
    match String.split_on_char '\t' string with
    | k :: v:: _ -> Some (k,v)
    | _ -> None

let decode string =
    string
    |> Str.global_replace (Str.regexp_string "\\t") "\t"
    |> Str.global_replace (Str.regexp_string "\\n") "\n"

let encode string =
  string
  |> Str.global_replace (Str.regexp_string "\t") "\\t"
  |> Str.global_replace (Str.regexp_string "\n") "\\n"

let getDB =
  let channel = open_in "db" in
  let output = 
    channel
      |> In_channel.input_lines
      |> List.filter_map parse
      |> StringMap.of_list
  in
  close_in channel;
  output

let write key value =
  let channel = open_out "db" in
  StringMap.fold
    (fun k v _ -> 
      Printf.fprintf channel "%s\n"
      ([k; v]|> String.concat "\t" )
    )
    (StringMap.add key value getDB)
    ();
  Out_channel.flush channel;
  close_out channel ;;

let read key =
  getDB
  |> StringMap.find key
  |> print_endline
  
  

