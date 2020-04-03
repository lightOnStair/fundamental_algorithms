open Lwt.Infix
let mut = Lwt_mutex.create ()

let sessions = ref [("",Lwt_io.null)]
exception Quit


let rec send_all sender msg =
Lwt_list.iter_p (fun (nick,out) -> if nick != sender
then (Lwt_io.printl (sender^": "^msg))
else Lwt.return ()) !sessions


let rec send_one sender receiver msg =
Lwt_list.iter_p (fun (nick,out) -> if nick=receiver
then (Lwt_io.printl ("hah~secret from "^sender^": "^msg))
else Lwt.return ()) !sessions


let remove_session nn =
  sessions := List.remove_assoc nn !sessions;
  send_all nn "<left chat>" >>= fun () ->
  Lwt.return ()


let handle_error e nn inp outp = remove_session nn


let change_nn nn outp new_nn =
  sessions := List.remove_assoc nn !sessions;
  sessions := ((new_nn,outp)::(!sessions));
  send_all nn ("<changed nick to "^new_nn^">") >>= fun () ->
  Lwt.return ()



let handle_login nr (inp,outp) =
Lwt_io.printl "Enter initial nick" >>= fun () ->
Lwt_io.read_line inp >>=
fun str -> nr := str;
Lwt_mutex.lock mut >>= fun () ->
sessions := (((!nr),outp)::!sessions);
Lwt.return (Lwt_mutex.unlock mut) >>=
fun () -> send_all !nr "<joined>"



let getinfor l =
let reals = String.sub l 3 (String.length l -1) in
let rec get acc i=
if String.get reals i != ' ' then get ((Char.escaped (String.get reals i)) ^ acc) (i+1)
else acc in
let name = get "" 0 in
let msg =
String.sub reals (String.length name -1) (String.length reals -1) in
(name,msg)




let handle_input nr outp l =
match String.sub l 0 2 with
| "/q" -> remove_session !nr
| "/n" -> change_nn !nr outp (String.sub l 3 ((String.length l) -1))
| "/l" -> Lwt_list.iter_s (fun (nick, cha) -> print_endline nick >>= fun () -> Lwt.return ())
| "/s" -> let infor = getinfor l in send_one !nr (fst infor) (snd infor)

send_all !nr l



let chat_server _ (inp,outp) =
  let nick = ref "" in
  let _ = handle_login nick (inp,outp) in
  let rec main_loop () =
	  Lwt_io.read_line inp >>= handle_input nick outp >>= main_loop in
  Lwt.catch main_loop (fun e -> handle_error e !nick inp outp)
