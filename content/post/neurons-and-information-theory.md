---
title: "Neurons and Information Theory"
date: 2023-01-30T14:10:22Z
draft: true
---

In a speech-turned-essay on Kafka, David Foster Wallace spoke of [_exformation_](https://en.wiktionary.org/wiki/exformation) as

{{<blockquote>}}
_A certain quantity of vital information removed from but evoked by a communication in such a way as to cause a kind of explosion of associative connections within the recipient._
{{</blockquote>}}

Something similar happens when understanding one thing in the domain of another. Mapping the thing from its original framework to another results in a burst of new relations, hopefully insightful. For instance, thinking of computer networks like brain networks, or thinking about topological continuity with physical-space-like intuitions like squeezing and stretching. The idea is that old associations in the new space become new associations that wouldn't have come up in the old space. A brilliant mapping to think about is that between neurons and information-theoretic channels.

Over the past year{{<sidenote>}}During an MRes{{</sidenote>}} I've had to think of this mapping a lot. How are neurons like channels? What information do they transmit? Why? There's loads of work in this vein{{<sidenote>}}See Further Reading{{</sidenote>}}, but what I want to do here is see how far we can get by thinking about these questions from first principles, working with what we (really, I) know of info-theory and neural coding. Nothing novel, but hopefully outlining the thought-process will be helpful for understanding -- like working out a math proof. Who knows, maybe even some exformation-like flashes of insight into the working of neurons.

## The Neural Code
Channels transmit information from a source to a target. They take some source symbols, encode them into code-words, and send them to the target, where they get decoded back into the original signal. At first glance, a neuron is similar in that it receives inputs (along its dendrites), then integrates them in a nonlinear process that concludes in action potentials (spikes).{{<sidenote>}}There's a conceptual _ouroboros_ here: the process that encodes inputs as spikes could also be thought of as -- on the post-synaptic neuron -- the one that decodes incoming spikes. Is there a distinction to be made, and where? Is it even _useful_ to make the en-/de-coding distinction here? (see Appendix A){{</sidenote>}} So here we assume the code-words are represented by the sequence of spikes emitted. So what are the code-words?{{<sidenote>}}If ever there were an eminent question in comp-neuro it was this one. No problem. We'll try to ignore the staggering amount of pre-existing thought on this -- for now -- and see how we can approach it by ourselves.{{</sidenote>}} Another way to ask: what differentiates code-words from each other? Without constraints, we can imagine _anything_ delineates: the number of spikes in a span of time, the time between two spikes, the ratio between the times between two pairs of spikes, the absolute time of a single spike relative to the start of the universe -- my point is, we need constraints to guide us in figuring out what the code may be. 

In the (pretty great) book [Spikes](https://mitpress.mit.edu/9780262181747/spikes/), Bialek and Co. point out the real-time constraints of neuronal processing. An animal needs to respond to external stimuli in a timely fashion. This means that neuronal code-words can't (or, at least are unlikely) to extend over long time-windows for most processing. We have our first constraint.

In the extreme, the fastest code-words would be over the smallest possible interval: the duration of a single action potential. In this case, all a neuron could communicate is the presence/absence of a single spike: 1 bit of information per unit time{{<sidenote>}}About 1-2ms, though variable{{</sidenote>}}. In this case each neuron would effectively be a kind of obscure logic gate, whose function is highly nonlinear, stochastic, and can change over time. The brain as a whole would be -- on the surface -- a lot like a digital computer.

Can a neuron transmit >1bit per unit time? If the window was longer, say 2-spikes long

## A time-extended code
Reading out a spike-train is like walking through binary code-space with time as a cost.

Let's say a single neuron has a 'memory' of $\tau$ milliseconds. Assuming a constant action-potential duration of about 1ms, each neuronal code-word communicates $\tau$ bits of information. A post-synaptic neuron doesn't integrate code-words in discrete chunks, jumping along a spike-train after reading one. Rather, it reads out the spike-train in a sliding window, incorporating the presence/absence of the next spike along with the prior spikes read. Thus, the code-words are sort of smeared out across the spike-train, for reading out in sequential slices. This kind of formulation factors in the influence of previous spikes on the state of the neuron: hysteresis.

Now, an abstract formulation of this is of code-words existing in a $\tau$ dimensional discrete space, each code-word occupying a position described by a $\tau$-length vector in this space. Reading out a spike-train, as described above, is then much like taking a walk in this space. Thinking geometrically, the largest distance between any two code-words scales with $\tau$. Additionally, the larger the space, the more information is communicable by the neuron. However, due to sequential readout, how quickly we can traverse the space is determined by how much time $t$ has elapsed; the full space of code-words is only available for $t \geq \tau$.

Given the real-time processing requirements on animal behaviour [CITE Bialek], we see that $t$ has a constraining effect on the size of code-space: that is, we have a trade-off between information rate and processing time, since crossing a larger code-space will cost more time.

### Continuous movement in code-space
When we consider incoming stimuli, we've assumed that source symbols are more or less uniformly random: two source symbols with code-words far apart in code-space could follow each other, thus the need for a $\tau$ that's shorter than the required processing time. However, we can weaken this constraint when we consider an encoding which reflects continuities in the source signal. If the source is non-uniform -- like, say, natural vision -- then the encoding can leverage this to utilise a much larger code-space than real-time dictates.

If the distance in code-space of two source symbols reflects their original distance, where by distance here we mean the likelihood of seeing the two in sequence, something like a bigram, and if this is true in general for all pairs of source symbols, then we can assert some maximum distance $\delta(t)$ in which a two code-words can differ, as a function of how long we read the code for. That is, we can get away with a read-time $t' < \tau$ because no two symbols will be further than $t'$ steps apart in code-space. Crucially, the symbols are _still_ being encoded in code-words with length $\tau$, these codes are reachable, but the continuity of source-space is leveraged to reduce read-time from what it would be. In summary: continuity/redundancy in source space can be utilised by the neuron to maximise the _information density_ of the neural code. 

### Accounting for noise
Code-words as spherical clouds in code-space, rather than exact points.

### Some predictions
1. Responses to stimuli with few redundancies (noise movies, sound, etc) the neuronal code will be less able to jump the time-distances in code-space, resulting in lower information transmitted per symbol relative to more-redundant stimuli. In other words, an increase in post-codeword-observation ambiguity about the source (noise entropy). 

### A variable time-extended code

## A protean neural code

Asking how the neuron communicates needs asking _why_. As far as information theory goes, most prevalent of theories is _efficient coding_: a neuron maximises

## Further Reading

## Appendices
### A. What decodes?
Decoding (in information theory) seems to assume the presence of a target for the signal who can understand the source signal, the signal in its original form. This notion maps poorly onto a neuron. The 'source signal' of vision is -- more or less -- the array of photons that strike photoreceptors in the eye. There's never a point in visual processing where this light-array is decoded from spikes. Rather, the light-signal undergoes successive encoding, transforming it into a form that makes organism-relevant information more explicit [CITE neural manifold stuff]. In this sense, a neuron never decodes anything.

We can zoom out and look at this through a more exotic lens, though, by thinking of consciousness. The contents of the visual qualia we experience are (implicitly) embedded in the light-array that meets our retinas. What the visual system does is disclose these contents, but perhaps a second process is involved in constructing the qualia as a whole: i.e. decode what the visual system encode. In other words, we would find encoding and decoding as qualitatively different processes in the brain.

I myself tend to steer away from such ideas, in favour of ones that account for the primacy of behaviour in determining the function of neural processing [CITE pre-motor paper and behaviour paper]. I'm not a cognitive scientist though, and there's likely good arguments on both fronts.


