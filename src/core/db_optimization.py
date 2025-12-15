"""
Database optimization utilities and helpers
"""
from django.db import models
from django.db.models import Q, QuerySet, Prefetch
from typing import List, Tuple, Optional
import logging

logger = logging.getLogger(__name__)


class BulkOperationHelper:
    """
    Helper class for performing bulk database operations efficiently
    Reduces database hits and improves performance for batch operations
    """
    
    @staticmethod
    def bulk_update_with_signals(model_class, objects: List, update_fields: List[str], batch_size: int = 100) -> int:
        """
        Bulk update objects while respecting Django signals
        Note: Django's bulk_update skips signals, so this alternative ensures signals are triggered
        
        Args:
            model_class: Django model class
            objects: List of model instances to update
            update_fields: List of field names to update
            batch_size: Number of objects to update per batch
            
        Returns:
            int: Number of objects updated
        """
        updated_count = 0
        
        for i in range(0, len(objects), batch_size):
            batch = objects[i:i + batch_size]
            for obj in batch:
                try:
                    obj.save(update_fields=update_fields)
                    updated_count += 1
                except Exception as e:
                    logger.error(f"Error updating {model_class.__name__}: {str(e)}")
                    continue
        
        return updated_count
    
    @staticmethod
    def bulk_create_optimized(model_class, objects: List, batch_size: int = 1000, ignore_conflicts: bool = True) -> List:
        """
        Bulk create objects with optimized batch size
        
        Args:
            model_class: Django model class
            objects: List of model instances to create
            batch_size: Number of objects to create per batch
            ignore_conflicts: Whether to ignore unique constraint conflicts
            
        Returns:
            List: List of created objects
        """
        created_objects = []
        
        for i in range(0, len(objects), batch_size):
            batch = objects[i:i + batch_size]
            try:
                created = model_class.objects.bulk_create(
                    batch,
                    batch_size=batch_size,
                    ignore_conflicts=ignore_conflicts
                )
                created_objects.extend(created)
                logger.info(f"Bulk created {len(created)} {model_class.__name__} objects")
            except Exception as e:
                logger.error(f"Error bulk creating {model_class.__name__}: {str(e)}")
                continue
        
        return created_objects
    
    @staticmethod
    def prefetch_with_filters(queryset: QuerySet, prefetch_config: List[Tuple[str, dict]]) -> QuerySet:
        """
        Apply prefetch_related with filtering for optimized queries
        
        Args:
            queryset: Django QuerySet to prefetch on
            prefetch_config: List of (relationship, filter_dict) tuples
                Example: [('members', {'is_active': True}), ('projects', {'featured': True})]
                
        Returns:
            QuerySet: Optimized queryset with prefetch applied
        """
        for relation, filters in prefetch_config:
            if filters:
                prefetch = Prefetch(
                    relation,
                    queryset=queryset.model._meta.get_field(relation).related_model.objects.filter(**filters)
                )
            else:
                prefetch = relation
            queryset = queryset.prefetch_related(prefetch)
        
        return queryset


class QueryOptimizationHelper:
    """
    Helper for analyzing and optimizing database queries
    """
    
    @staticmethod
    def count_queries_in_context(queryset: QuerySet) -> int:
        """
        Estimate number of database queries for a queryset
        Useful for testing N+1 query problems
        
        Args:
            queryset: Django QuerySet to analyze
            
        Returns:
            int: Estimated number of queries
        """
        # This is a simple estimate - actual count requires testing with Django debug toolbar
        return 1 + sum(len(prefetch.prefetch_through) for prefetch in queryset.query.prefetch_related_lookups)
    
    @staticmethod
    def optimize_queryset(queryset: QuerySet, select_related: List[str] = None, 
                         prefetch_related: List[str] = None) -> QuerySet:
        """
        Apply standard optimizations to a queryset
        
        Args:
            queryset: Django QuerySet to optimize
            select_related: List of foreign key/one-to-one relations
            prefetch_related: List of many-to-many/reverse foreign key relations
            
        Returns:
            QuerySet: Optimized queryset
        """
        if select_related:
            queryset = queryset.select_related(*select_related)
        
        if prefetch_related:
            queryset = queryset.prefetch_related(*prefetch_related)
        
        return queryset
