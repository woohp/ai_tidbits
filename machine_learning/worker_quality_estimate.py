import scipy as sp
from scipy.stats.mstats import mode

def worker_quality(predictions, num_classes):
    predictions = sp.atleast_2d(predictions)
    num_workers, num_objects = predictions.shape

    error_rates = sp.zeros((num_workers, num_classes, num_classes))
    diy, diz = sp.diag_indices(num_classes)
    error_rates[:, diy, diz] = 1

    while True:
        # E step
        new_predictions = sp.zeros((num_objects, num_classes))
        for i in xrange(num_objects):
            individual_predictions = predictions[:, i]
            individual_error_rates = error_rates[range(num_workers), individual_predictions, individual_predictions]
            new_predictions[i, :] = sp.bincount(individual_predictions, individual_error_rates, minlength=num_classes)

        correct_labels = sp.argmax(new_predictions, axis=1)
        count_per_label = sp.bincount(correct_labels)

        # M step
        new_error_rates = sp.zeros((num_workers, num_classes, num_classes))
        for i, label in enumerate(correct_labels):
            new_error_rates[range(num_workers), label, predictions[:, i]] += 1

        for i in xrange(num_classes):
            new_error_rates[:, :, i] /= count_per_label

        diff_error_rates = sp.absolute(new_error_rates - error_rates)
        error_rates = new_error_rates

        if sp.amax(diff_error_rates) < 0.001:
            break


    # calculate the cost of each worker
    class_priors = sp.bincount(correct_labels, minlength=num_classes) / float(num_objects)
    costs = []
    for k in xrange(num_workers):
        worker_class_priors = sp.dot(sp.atleast_2d(class_priors), error_rates[k])[0] + 0.0000001

        cost = 0
        for j in xrange(num_classes):
            soft_label = error_rates[k, :, j] * class_priors / worker_class_priors[j]

            soft_label_cost = 0.0
            for i in xrange(num_classes):
                soft_label_cost += sp.sum(soft_label[i] * soft_label)
            soft_label_cost -= sp.sum(soft_label ** 2) # subtract the diagonal entries (those costs = 0)
            cost += soft_label_cost * worker_class_priors[j]

        costs.append(cost)

    return error_rates, correct_labels, costs


#num_workers = 200
#num_classes = 5
#num_objects = 5000
#error_rates = sp.random.random_integers(2, 30, (num_workers, num_classes, num_classes)).astype(sp.float64)
#diy, diz = sp.diag_indices(num_classes)
#error_rates[:, diy, diz] = 50
#for i in xrange(num_workers):
#    error_rates[i, :, :] /= sp.sum(error_rates[i, :, :], axis=1)
#print error_rates[0]
#
#true_labels = sp.random.random_integers(0, num_classes-1, num_objects)
#predictions = []
#for i in xrange(num_workers):
#    worker_predictions = []
#    for label in true_labels:
#        prediction = error_rates[i, label].cumsum().searchsorted(sp.random.sample(1))[0]
#        if prediction == 5:
#            prediction = 4
#        worker_predictions.append(prediction)
#    predictions.append(worker_predictions)

num_workers = 5
num_classes = 2
num_objects = 5
true_labels = [0, 1, 0, 1, 0]
predictions = [
        [1, 1, 1, 1, 1],
        [0, 1, 0, 1, 1],
        [0, 1, 0, 1, 0],
        [0, 1, 0, 1, 0],
        [1, 0, 1, 0, 1]]

predictions = sp.array(predictions)
est_error_rates, est_correct_labels, est_costs = worker_quality(predictions, num_classes)
print 'estimated worker confusion matrix:'
print est_error_rates
print 'estimated correct labels:', est_correct_labels
print 'estimated costs:', est_costs
