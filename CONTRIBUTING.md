# Contributing to Threshold Fairness Lab

Thank you for your interest in contributing to the Threshold Fairness Lab! We welcome contributions from researchers, economists, and developers.

## Important Mathematical Rule

The core engine (`/core`) of this tool implements a strict, verified mathematical model regarding pure-strategy Nash equilibria, strict coalition stability, and probabilistic reliability. 

**Do NOT submit PRs that:**
- Introduce arbitrary heuristic "security scores"
- Break the independent Bernoulli probability assumptions without explicitly updating the mathematical specification
- Replace exact enumeration with Monte Carlo simulation for `n <= 8`

If you find a genuine mathematical bug in the core engine, please open an Issue with the formal mathematical derivation before submitting a PR.

## How to Contribute

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Write your feature
4. **Write tests** in `/tests` for any core engine changes
5. Run the existing tests (`pytest`)
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request
