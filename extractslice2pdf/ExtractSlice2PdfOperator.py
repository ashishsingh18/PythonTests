from datetime import timedelta
from kaapana.operators.KaapanaBaseOperator import KaapanaBaseOperator
from kaapana.blueprints.kaapana_global_variables import (
    DEFAULT_REGISTRY,
    KAAPANA_BUILD_VERSION,
)
from kaapana.kubetools.resources import Resources as PodResources

class ExtractSlice2PdfOperator(KaapanaBaseOperator):

    execution_timeout=timedelta(minutes=60)

    def __init__(self,
                 dag,
                 env_vars=None,
                 execution_timeout=execution_timeout,
                 *args, **kwargs
                 ):

        if env_vars is None:
            env_vars = {}

        pod_resources = PodResources(request_memory=None, request_cpu=None, limit_memory=None, limit_cpu=None, limit_gpu=None)

        super().__init__(
            dag=dag,
            name='extract_slice_to_pdf',
            env_vars=env_vars,
            image=f"{DEFAULT_REGISTRY}/extractslice2pdf:0.1.2",
            #image="{}{}/combine_labels:0.1.0".format(default_registry, default_project),
            #pod_resources=pod_resources,
            image_pull_secrets=["registry-secret"],
            execution_timeout=execution_timeout,
            *args,
            **kwargs
        )
