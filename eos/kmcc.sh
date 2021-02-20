cleos wallet create -n kmcc.wallet -f kmcc.wallet

# token
cleos wallet import -n kmcc.wallet --private-key 5KkbNdD4e46m8MyD3VDBGF64x4wZ8HzJ66o4jaf5fmVBJdo6vMd
cleos wallet import -n kmcc.wallet --private-key 5HwDQK9bD6m18ZsFSp44TzMfmMp2TDn7gkh57CyFQXKX1DisYpp
# auction
cleos wallet import -n kmcc.wallet --private-key 5KXCjKiKVTQdJnfUTT2pMqkc7ENNz9fDEgACoHFKDFwGdjtjC64
cleos wallet import -n kmcc.wallet --private-key 5K3VgB3GpPY4n9iGiMiiaJXgxsZGTt1PSGptG2Ud7H1kvfZnp1A
# flip
cleos wallet import -n kmcc.wallet --private-key 5KP75m4vbckJjqrFkJgRRPDbKbnpKjmwmFhzvbhuH7oMMmds24g
cleos wallet import -n kmcc.wallet --private-key 5JaYD7WkQRzkCm5dwEvDeoVVEU7stP5ujbPgb7veXiFNyrhHTTS
# team
cleos wallet import -n kmcc.wallet --private-key 5JN1jFeaMQg1sGRDJndDAmKyKen8ncXy3L9ptqNkdt75ur9wvme
cleos wallet import -n kmcc.wallet --private-key 5JtqyhNooa2gmS3j3DNxrAHHqRfsCCi5E9H9pVfXSKEjDME717t

# unlock wallet
cleos wallet unlock -n kmcc.wallet --password PW5JrCub8bHvVC1iFFqhC7d6pbVudMTLE3nWFCbxbSAksndWQALGX
# set permission with public key
# flip
cleos set account permission kmccgameflip active '{"threshold":1,"keys":[{"key":"EOS5PxCFjRaRHFHoze3Kzb5NzW8QbLGekLxeQjgZWhPrbZ9G3MxmC","weight":1}],"accounts":[{"permission":{"actor":"eosio.token","permission":"eosio.code"},"weight":1},{"permission":{"actor":"kmccauctions","permission":"eosio.code"},"weight":1},{"permission":{"actor":"kmccgameflip","permission":"eosio.code"},"weight":1}]}' owner
# auction
cleos set account permission kmccauctions active '{"threshold":1,"keys":[{"key":"EOS8mjvyTZt3CyLQm2fVofqFZA77uqVuyFYMcKJzYYnqtZLMBpLKJ","weight":1}],"accounts":[{"permission":{"actor":"eosio.token","permission":"eosio.code"},"weight":1},{"permission":{"actor":"kmccauctions","permission":"eosio.code"},"weight":1}]}' owner
# token
cleos set account permission kmccfliptoke active '{"threshold":1,"keys":[{"key":"EOS7BSKuzG8Hpn34s2eFvGDugHL8LAWQfxTaR4MFZvfriwRvVcN2u","weight":1}],"accounts":[{"permission":{"actor":"eosio.token","permission":"eosio.code"},"weight":1},{"permission":{"actor":"kmccfliptoke","permission":"eosio.code"},"weight":1},{"permission":{"actor":"kmccgameflip","permission":"eosio.code"},"weight":1}]}' owner

# set contract to kmccfliptoke
cleos set contract kmccfliptoke eosio.token

# create token 
cleos push action kmccfliptoke create '["kmccfliptoke", "8800000000.0000 MCC", 1, 1, 1]' -p kmccfliptoke

# issue token
cleos push action kmccfliptoke issue '["kmccgameflip", "10000000.0000 MCC", "issue MCC"]' -p kmccfliptoke

# init global vars
cleos push action kmccgameflip init '[]' -p kmccgameflip
cleos push action kmccauctions setgbvars '[]' -p kmccauctions

# buyram
cleos system buyram payer receiver -k 5120

# delegatebw
cleos system delegatebw payer receiver "10.0000 EOS" "10.0000 EOS"