cat k8s/readme.md  |\
grep "^#" |\
sed 's|^[ ]*||g' |\
awk  -F, '\
BEGIN {
}{
  basic_name=$1;
  anchor=basic_name
  basic_name_no_hash=basic_name
  gsub(/^[#]* /,"",basic_name_no_hash)
  gsub(/[ ]*$/,"",basic_name_no_hash)
  subs_string=basic_name
  subs = gsub(/#/,"",subs_string);
  gsub(/^[#]+ /,"",anchor);
  gsub(/ /,"-",anchor);
  anchor = tolower(anchor);
  {for (i=0;i<subs-1;i++) printf "    " }
  print "* [" basic_name_no_hash "](https://github.com/mixa2130/docker_setups/blob/master/k8s/README.md#" anchor ")";
}
END {
}'