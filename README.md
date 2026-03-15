# DARDS
Decision-Aware Risk &amp; Deployment System — a machine learning decision framework for capital deployment and risk posture determination.

## Executive summary

DARDS organises observed market behaviour into a structured capital allocation decision. The system evaluates market conditions and determines an appropriate capital posture and risk budget for the portfolio.

Financial markets present incomplete and unstable information. Returns are noisy, correlations change and volatility regimes shift. Portfolio exposure therefore requires continuous reassessment as new evidence appears. DARDS structures the information used in allocation decisions so that exposure adjusts with the observed state of the market.

The framework begins with observed returns across a small universe of assets. From these returns it derives signals describing persistence of movement, realised volatility and the joint behaviour of assets. These signals describe the environment in which the portfolio operates and indicate whether relationships between assets appear stable or unstable.

The signals feed into a decision layer that determines the prevailing capital posture. This posture expresses the level of exposure appropriate under current conditions. Portfolio weights follow through volatility aware allocation that balances expected opportunity, diversification and implementation stability. The resulting output provides a transparent link between market evidence and portfolio exposure.

The framework serves as a structured input to judgement. It presents exposure, risk context and allocation choices within a single analytical structure that supports discussion among portfolio management, risk and engineering stakeholders.

## Decision process

The system follows a sequence consistent with how portfolio exposure is typically evaluated.

Market behaviour is observed through price series and converted into returns.

Signals are constructed from those returns. These include persistence of movement, realised volatility and correlation structure.

The signals define the prevailing risk regime and capital posture.

The posture determines the risk budget available to the portfolio.

Portfolio weights follow through volatility aware allocation that reflects opportunity and diversification.

The system produces a desk brief that summarises posture, signal drivers and portfolio weights.

Exposure evolves as new market information enters the system.

## Technical overview

Capital allocation operates as a sequential decision process. Market behaviour is observed first. Signals provide context. Portfolio exposure follows from the interpretation of those signals. DARDS implements this structure through a modular pipeline.

The process begins with a market snapshot assembled from price series. Returns form the core state variable used across the system. From these returns the system constructs several signals. Medium horizon persistence measures the stability of recent price movement. Realised volatility measures prevailing risk conditions. Correlation structure describes how assets move together and whether diversification strengthens or weakens. A composite pressure signal summarises these elements and characterises the broader market environment.

A decision layer interprets the signals and determines the current risk regime together with the appropriate capital posture. The system identifies environments where capital deployment expands, contracts or remains neutral. Confidence reflects the stability and agreement of the signals informing that decision.

The allocation engine converts the posture into portfolio weights. Volatility aware sizing and risk budgeting maintain proportional exposure across assets. Allocation reflects opportunity, diversification and trading stability.

Evaluation occurs through rolling backtests and controlled stress scenarios. Historical crisis periods and stylised shocks illustrate how the decision framework behaves when relationships between assets deteriorate. These exercises provide a view of the system’s behaviour across varying conditions.

Outputs appear as a desk brief summarising posture, signal drivers and resulting allocations. Each run is archived so that decisions remain traceable and reproducible over time.

## Repository structure

The repository separates each stage of the decision process.

1. configs

System parameters and configuration

2. data

Market data assembly validation and schema

3. features

Signal construction including persistence, volatility, correlation and pressure

4. engine

Decision logic, risk budgeting, allocation and backtesting

5. reporting

Desk brief generation, performance reporting and run archiving

6. stress

Scenario definitions and stress harness

## Example output

Each execution produces a decision summary similar to the following.

DARDS Capital Posture Brief

Posture: neutral
Risk regime: neutral
Confidence: high

Drivers
SPY return: 0.0076
TLT return: 0.0012
Correlation regime: neutral
Risk pressure: -0.22

Interpretation
Capital posture set to neutral under balanced conditions with moderate exposure.
Risk budget multiplier: 0.89

The desk brief presents the information required for review of the exposure decision and its underlying signals.

## Intended use

DARDS demonstrates how market observations can be organised into a structured exposure decision. The framework provides transparency for the humans responsible for capital oversight.

In practice such systems operate within governance structures that include independent validation, risk limits and operational review. The framework therefore functions as an analytical tool that clarifies the relationships driving allocation and the implications for portfolio exposure.

## Perspective

Capital allocation depends on relationships that evolve through time. Signals lose stability and market structure changes. DARDS provides a structured way to interpret market behaviour so that exposure decisions remain coherent as conditions change.

The framework organises information and clarifies the assumptions underlying allocation choices. Its value lies in supporting informed discussion among the stakeholders responsible for capital, risk and implementation.
