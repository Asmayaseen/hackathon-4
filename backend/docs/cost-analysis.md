# Cost Analysis — Phase 1: Zero-Backend-LLM

**Date**: 2026-03-09
**Scale**: 10,000 Monthly Active Users

## Phase 1 Infrastructure Cost Breakdown

| Component | Provider | Pricing Model | Monthly (10k MAU) |
|-----------|----------|--------------|-------------------|
| Content Storage | Cloudflare R2 | $0.015/GB + $0.36/M reads | ~$5 |
| Database | Neon (PostgreSQL) | Free tier → $19/mo | $0–$19 |
| Compute | Fly.io | shared-cpu-1x, 256MB | ~$10 |
| Domain + SSL | Namecheap + Fly | ~$12/year | ~$1 |
| **TOTAL** | | | **$16–$35** |

**Cost per user per month**: $0.002–$0.004

## ChatGPT Usage Cost

**$0 to the developer.**

Users access the Course Companion FTE through their own ChatGPT subscription.
The developer pays zero LLM inference costs in Phase 1.

This is the Zero-Backend-LLM advantage.

## Comparison: Human Tutor vs Course Companion FTE

| Metric | Human Tutor | Course Companion FTE |
|--------|------------|---------------------|
| Availability | 40 hrs/week | 168 hrs/week (24/7) |
| Monthly Cost | $2,000–$5,000 | $16–$35 (infrastructure) |
| Students Served | 20–50 | Unlimited (concurrent) |
| Cost per Session | $25–$100 | ~$0.004 (infrastructure only) |
| Consistency | 85–95% | 99%+ (deterministic) |
| Languages | 1–3 | 50+ (via ChatGPT) |

## Phase 2 Cost Projection (Hybrid Intelligence)

When Phase 2 premium features are added:

| Feature | Model | Tokens/Request | Cost/Request |
|---------|-------|---------------|-------------|
| Adaptive Learning Path | Claude Sonnet | ~2,000 | $0.018 |
| LLM-Graded Assessments | Claude Sonnet | ~1,500 | $0.014 |

Phase 2 features are gated behind:
- **Premium tier** ($9.99/mo) — for Adaptive Learning Path
- **Pro tier** ($19.99/mo) — for LLM Assessments + Adaptive Path

At $0.018/request and 100 requests/user/month, Phase 2 adds ~$1.80/premium user/month.
With $9.99/mo revenue, margin remains strong.

## Monetisation Tiers

| Tier | Price | Features |
|------|-------|---------|
| Free | $0 | Chapters 1–3, basic quizzes, ChatGPT tutoring |
| Premium | $9.99/mo | All 5 chapters, all quizzes, progress tracking |
| Pro | $19.99/mo | Premium + Adaptive Path + LLM Assessments |
| Team | $49.99/mo | Pro + Analytics + Multiple seats |

## Break-Even Analysis

At 100 Premium subscribers ($999/month revenue):
- Infrastructure ($35) + Phase 2 LLM costs (~$180) = $215/month
- **Net margin**: $784/month (78%)

At 1,000 Premium subscribers: ~$9,990/month revenue, ~$2,000 costs → 80% margin.

## Scaling Projections

| Users | Infra Cost | ChatGPT Cost | Total | Cost/User |
|-------|-----------|-------------|-------|-----------|
| 1,000 | $16 | $0 | $16 | $0.016 |
| 10,000 | $35 | $0 | $35 | $0.0035 |
| 100,000 | $150 | $0 | $150 | $0.0015 |

Zero-Backend-LLM enables near-linear cost at sub-linear growth — the infrastructure
cost grows much slower than the user base.
