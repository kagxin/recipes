
def averager():
    total = 0.0
    count = 0
    average = None
    while True:
        term = yield average
        if term==None:
            break
        total += term
        count += 1
        average = total/count
    return count, average

cor = averager()
cor.send(None)
print(cor.send(1))
print(cor.send(2))
try:
    cor.send(None)
except StopIteration as e:
    print(e.value)

def grouper(result, key):
    while True:
        result[key] = yield  from averager()

def main(data):
    results = {}
    for key, values in data.items():
        group = grouper(results, key)
        next(group)
        for value, in values:
            group.send(value)
    report(results)

def report(results):
    for key, result in sorted(results.items()):
        group, unit = key.split(';')
        print('{:2} {:5} averaging {:.2f}{}'.format(result.count, group, result.average, unit))

data = {

}