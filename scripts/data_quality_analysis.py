#!/usr/bin/env python3
"""
Data Quality Analysis Script - Part 1 Requirement
Analyzes orders_sample.ndjson and answers all 5 required questions
"""

import json
import sys
from pathlib import Path
from collections import Counter, defaultdict
from typing import Dict, List, Any

# Add src to path
sys.path.append(str(Path(__file__).parent.parent))

from src.models.order import Order
from pydantic import ValidationError


def load_and_validate_orders(file_path: str) -> tuple[List[Order], List[Dict], List[str]]:
    """Load orders and separate into accepted vs rejected"""
    accepted = []
    rejected = []
    rejection_reasons = []
    
    with open(file_path, 'r') as f:
        for line_num, line in enumerate(f, 1):
            if not line.strip():
                continue
            try:
                data = json.loads(line)
                order = Order(**data)
                accepted.append(order)
            except (json.JSONDecodeError, ValidationError) as e:
                rejected.append(data)
                rejection_reasons.append(f"Line {line_num}: {str(e)[:100]}")
    
    return accepted, rejected, rejection_reasons


def analyze_acceptance_rate(accepted: List, rejected: List) -> Dict:
    """Question 1: Overall Acceptance Rate"""
    total = len(accepted) + len(rejected)
    acceptance_rate = len(accepted) / total if total > 0 else 0
    
    return {
        "total_records": total,
        "accepted": len(accepted),
        "rejected": len(rejected),
        "acceptance_rate": f"{acceptance_rate:.2%}"
    }


def analyze_field_profiles(accepted: List[Order]) -> Dict:
    """Question 2: Per-Field Basic Profiles"""
    profiles = {}
    
    # Status field
    statuses = [o.status for o in accepted]
    profiles["status"] = {
        "count": len(statuses),
        "distinct_values": len(set(statuses)),
        "value_distribution": dict(Counter(statuses))
    }
    
    # Quantity field
    quantities = [o.quantity for o in accepted]
    profiles["quantity"] = {
        "count": len(quantities),
        "min": min(quantities),
        "max": max(quantities),
        "distinct_values": len(set(quantities))
    }
    
    # Unit Price field
    prices = [o.unit_price for o in accepted]
    profiles["unit_price"] = {
        "count": len(prices),
        "min": f"${min(prices):.2f}",
        "max": f"${max(prices):.2f}",
        "distinct_values": len(set(prices))
    }
    
    # Country Code
    countries = [o.shipping.country_code for o in accepted if o.shipping]
    profiles["country_code"] = {
        "count": len(countries),
        "distinct_values": len(set(countries)),
        "value_distribution": dict(Counter(countries))
    }
    
    return profiles


def analyze_missing_values(accepted: List[Order]) -> Dict:
    """Question 3: Missing/Unusable Values"""
    missing_analysis = {}
    
    # Tags (optional field)
    missing_tags = sum(1 for o in accepted if not o.tags or len(o.tags) == 0)
    missing_analysis["tags"] = {
        "total_records": len(accepted),
        "missing_count": missing_tags,
        "missing_percentage": f"{(missing_tags/len(accepted)*100):.1f}%"
    }
    
    # Coupon Code (optional field)
    missing_coupon = sum(1 for o in accepted if not o.coupon_code)
    missing_analysis["coupon_code"] = {
        "total_records": len(accepted),
        "missing_count": missing_coupon,
        "missing_percentage": f"{(missing_coupon/len(accepted)*100):.1f}%"
    }
    
    # Is Gift (optional field)
    missing_gift = sum(1 for o in accepted if o.is_gift is None)
    missing_analysis["is_gift"] = {
        "total_records": len(accepted),
        "missing_count": missing_gift,
        "missing_percentage": f"{(missing_gift/len(accepted)*100):.1f}%"
    }
    
    return missing_analysis


def analyze_outliers(accepted: List[Order]) -> Dict:
    """Question 4: Outliers and Extreme Values"""
    quantities = [o.quantity for o in accepted]
    prices = [o.unit_price for o in accepted]
    
    # Define extreme thresholds
    EXTREME_QTY_LOW = 0
    EXTREME_QTY_HIGH = 10
    EXTREME_PRICE_LOW = 5.0
    EXTREME_PRICE_HIGH = 20.0
    
    extreme_qty = [q for q in quantities if q <= EXTREME_QTY_LOW or q >= EXTREME_QTY_HIGH]
    extreme_prices = [p for p in prices if p <= EXTREME_PRICE_LOW or p >= EXTREME_PRICE_HIGH]
    
    return {
        "quantity": {
            "min": min(quantities),
            "max": max(quantities),
            "extreme_threshold": f"<= {EXTREME_QTY_LOW} or >= {EXTREME_QTY_HIGH}",
            "extreme_count": len(extreme_qty),
            "extreme_percentage": f"{(len(extreme_qty)/len(quantities)*100):.1f}%"
        },
        "unit_price": {
            "min": f"${min(prices):.2f}",
            "max": f"${max(prices):.2f}",
            "extreme_threshold": f"<= ${EXTREME_PRICE_LOW} or >= ${EXTREME_PRICE_HIGH}",
            "extreme_count": len(extreme_prices),
            "extreme_percentage": f"{(len(extreme_prices)/len(prices)*100):.1f}%"
        }
    }


def analyze_quality_by_grouping(accepted: List[Order], rejected: List[Dict]) -> Dict:
    """Question 5: Quality by Grouping"""
    # Group by status
    status_groups = defaultdict(lambda: {"total": 0, "accepted": 0, "rejected": 0})
    
    # Count accepted by status
    for order in accepted:
        status_groups[order.status]["total"] += 1
        status_groups[order.status]["accepted"] += 1
    
    # Count rejected by status (if status field exists)
    for data in rejected:
        status = data.get("status", "unknown")
        status_groups[status]["total"] += 1
        status_groups[status]["rejected"] += 1
    
    # Calculate acceptance rates
    result = {}
    for status, counts in status_groups.items():
        acceptance_rate = counts["accepted"] / counts["total"] if counts["total"] > 0 else 0
        result[status] = {
            "total_records": counts["total"],
            "accepted": counts["accepted"],
            "rejected": counts["rejected"],
            "acceptance_rate": f"{acceptance_rate:.2%}"
        }
    
    return result


def generate_report(analysis_results: Dict) -> str:
    """Generate markdown report"""
    report = """# Data Quality Analysis Report

## Executive Summary
This report analyzes the `orders_sample.ndjson` dataset and answers the 5 required data quality questions.

---

## Question 1: Overall Acceptance Rate

**Total Records Processed:** {total_records}
- **Accepted:** {accepted} records
- **Rejected:** {rejected} records
- **Acceptance Rate:** {acceptance_rate}

---

## Question 2: Per-Field Basic Profiles

### Status Field
- **Count:** {status_count}
- **Distinct Values:** {status_distinct}
- **Distribution:**
{status_dist}

### Quantity Field
- **Count:** {qty_count}
- **Min:** {qty_min}
- **Max:** {qty_max}
- **Distinct Values:** {qty_distinct}

### Unit Price Field
- **Count:** {price_count}
- **Min:** {price_min}
- **Max:** {price_max}
- **Distinct Values:** {price_distinct}

### Country Code Field
- **Count:** {country_count}
- **Distinct Values:** {country_distinct}
- **Distribution:**
{country_dist}

---

## Question 3: Missing/Unusable Values

### Tags Field
- **Total Records:** {tags_total}
- **Missing Count:** {tags_missing}
- **Missing Percentage:** {tags_pct}

### Coupon Code Field
- **Total Records:** {coupon_total}
- **Missing Count:** {coupon_missing}
- **Missing Percentage:** {coupon_pct}

### Is Gift Field
- **Total Records:** {gift_total}
- **Missing Count:** {gift_missing}
- **Missing Percentage:** {gift_pct}

---

## Question 4: Outliers and Extreme Values

### Quantity Field
- **Minimum:** {qty_outlier_min}
- **Maximum:** {qty_outlier_max}
- **Extreme Threshold:** {qty_threshold}
- **Extreme Count:** {qty_extreme_count}
- **Extreme Percentage:** {qty_extreme_pct}

### Unit Price Field
- **Minimum:** {price_outlier_min}
- **Maximum:** {price_outlier_max}
- **Extreme Threshold:** {price_threshold}
- **Extreme Count:** {price_extreme_count}
- **Extreme Percentage:** {price_extreme_pct}

---

## Question 5: Quality by Grouping (Status)

{quality_by_status}

---

## Conclusion

The dataset shows a **{acceptance_rate}** acceptance rate with {rejected} rejected records out of {total_records} total.
Key findings:
- Most common status: {most_common_status}
- {tags_pct} of records are missing tags
- {qty_extreme_pct} of records have extreme quantity values

This analysis provides the foundation for data-driven decision making in the logistics pipeline.
"""
    
    # Format status distribution
    status_dist = "\n".join([f"  - `{k}`: {v} records" for k, v in analysis_results["field_profiles"]["status"]["value_distribution"].items()])
    country_dist = "\n".join([f"  - `{k}`: {v} records" for k, v in analysis_results["field_profiles"]["country_code"]["value_distribution"].items()])
    
    # Format quality by grouping
    quality_lines = []
    for status, data in analysis_results["quality_by_grouping"].items():
        quality_lines.append(f"### Status: `{status}`")
        quality_lines.append(f"- **Total Records:** {data['total_records']}")
        quality_lines.append(f"- **Accepted:** {data['accepted']}")
        quality_lines.append(f"- **Rejected:** {data['rejected']}")
        quality_lines.append(f"- **Acceptance Rate:** {data['acceptance_rate']}\n")
    
    most_common_status = max(analysis_results["field_profiles"]["status"]["value_distribution"].items(), key=lambda x: x[1])[0]
    
    return report.format(
        total_records=analysis_results["acceptance_rate"]["total_records"],
        accepted=analysis_results["acceptance_rate"]["accepted"],
        rejected=analysis_results["acceptance_rate"]["rejected"],
        acceptance_rate=analysis_results["acceptance_rate"]["acceptance_rate"],
        
        status_count=analysis_results["field_profiles"]["status"]["count"],
        status_distinct=analysis_results["field_profiles"]["status"]["distinct_values"],
        status_dist=status_dist,
        
        qty_count=analysis_results["field_profiles"]["quantity"]["count"],
        qty_min=analysis_results["field_profiles"]["quantity"]["min"],
        qty_max=analysis_results["field_profiles"]["quantity"]["max"],
        qty_distinct=analysis_results["field_profiles"]["quantity"]["distinct_values"],
        
        price_count=analysis_results["field_profiles"]["unit_price"]["count"],
        price_min=analysis_results["field_profiles"]["unit_price"]["min"],
        price_max=analysis_results["field_profiles"]["unit_price"]["max"],
        price_distinct=analysis_results["field_profiles"]["unit_price"]["distinct_values"],
        
        country_count=analysis_results["field_profiles"]["country_code"]["count"],
        country_distinct=analysis_results["field_profiles"]["country_code"]["distinct_values"],
        country_dist=country_dist,
        
        tags_total=analysis_results["missing_values"]["tags"]["total_records"],
        tags_missing=analysis_results["missing_values"]["tags"]["missing_count"],
        tags_pct=analysis_results["missing_values"]["tags"]["missing_percentage"],
        
        coupon_total=analysis_results["missing_values"]["coupon_code"]["total_records"],
        coupon_missing=analysis_results["missing_values"]["coupon_code"]["missing_count"],
        coupon_pct=analysis_results["missing_values"]["coupon_code"]["missing_percentage"],
        
        gift_total=analysis_results["missing_values"]["is_gift"]["total_records"],
        gift_missing=analysis_results["missing_values"]["is_gift"]["missing_count"],
        gift_pct=analysis_results["missing_values"]["is_gift"]["missing_percentage"],
        
        qty_outlier_min=analysis_results["outliers"]["quantity"]["min"],
        qty_outlier_max=analysis_results["outliers"]["quantity"]["max"],
        qty_threshold=analysis_results["outliers"]["quantity"]["extreme_threshold"],
        qty_extreme_count=analysis_results["outliers"]["quantity"]["extreme_count"],
        qty_extreme_pct=analysis_results["outliers"]["quantity"]["extreme_percentage"],
        
        price_outlier_min=analysis_results["outliers"]["unit_price"]["min"],
        price_outlier_max=analysis_results["outliers"]["unit_price"]["max"],
        price_threshold=analysis_results["outliers"]["unit_price"]["extreme_threshold"],
        price_extreme_count=analysis_results["outliers"]["unit_price"]["extreme_count"],
        price_extreme_pct=analysis_results["outliers"]["unit_price"]["extreme_percentage"],
        
        quality_by_status="\n".join(quality_lines),
        most_common_status=most_common_status
    )


def main():
    print("🔍 Starting Data Quality Analysis...\n")
    
    # Load and validate
    file_path = "data/raw/orders_sample.ndjson"
    accepted, rejected, reasons = load_and_validate_orders(file_path)
    
    print(f"✅ Loaded {len(accepted)} accepted orders")
    print(f"❌ Rejected {len(rejected)} orders\n")
    
    # Run all analyses
    analysis_results = {
        "acceptance_rate": analyze_acceptance_rate(accepted, rejected),
        "field_profiles": analyze_field_profiles(accepted),
        "missing_values": analyze_missing_values(accepted),
        "outliers": analyze_outliers(accepted),
        "quality_by_grouping": analyze_quality_by_grouping(accepted, rejected)
    }
    
    # Generate report
    report = generate_report(analysis_results)
    
    # Save report
    output_path = "reports/data_quality_report.md"
    Path("reports").mkdir(exist_ok=True)
    with open(output_path, 'w') as f:
        f.write(report)
    
    print(f"📊 Report generated: {output_path}")
    print("\n" + "="*80)
    print(report)


if __name__ == "__main__":
    main()
