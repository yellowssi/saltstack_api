from api.salt_api import SaltAPI


client = SaltAPI('192.168.56.102', 8080, 'saltapi', 'yellowsea')
# print(client.compound_cmd('G@roles:webserver', 'test.fib', '10000000'))
# response = client.compound_async_cmd('G@roles:webserver', 'test.fib', '10000000')
# response = client.compound_async_cmd('G@roles:database', 'cmd.run', 'ifconfig')
# print(response)
print(client.list_running_jobs())
# print(client.get_jid_ret(response['jid']))
# print(client.list_all_key())
# print(client.get_job_status('20181116143911148367'))
print(client.get_jid_ret('20181116143911148367'))
